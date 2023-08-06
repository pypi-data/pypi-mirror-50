import os
# import json
from pathlib import Path
from gdbuild.file_helper import FileHelper


# Default Export Names
class ExportPlatforms:
    WINDOWS = "Windows Desktop"
    MACOSX = "Mac OSX"
    LINUX = "Linux/X11"


class Platforms:
    WINDOWS = "Windows"
    MACOSX = "MacOSX"
    LINUX = "Linux"


class Data:

    PLATFORM = 0
    FILE_EXT = 1

    template_platform_data = {
        Platforms.WINDOWS: {
            PLATFORM: Platforms.WINDOWS,
            FILE_EXT: ".exe"
        },
        Platforms.MACOSX: {
            PLATFORM: Platforms.MACOSX,
            FILE_EXT: "_zip"
        },
        Platforms.LINUX: {
            PLATFORM: Platforms.LINUX,
            FILE_EXT: ".x86_64"
        },
    }

    def get_default_platform_data(self, key):
        return self.template_platform_data[key].copy()


class GDBuild:
    SUCCESS = "SUCCESS"
    FAILURE = "FAILURE"
    export_platforms = ExportPlatforms()
    file_helper = FileHelper()

    def __init__(
            self, project_path, build_path, game_name, godot_file_path, export_debug=False,
            windows_build_name=None, macosx_build_name=None, linux_build_name=None,
            create_zip=True, test=False, execute_build_on_init=False
            ):
        self.project_path = project_path
        self.build_path = build_path
        self.game_name = game_name
        self.godot_file_path = godot_file_path
        self.export_debug = export_debug
        self.windows_build_name = windows_build_name
        self.macosx_build_name = macosx_build_name
        self.linux_build_name = linux_build_name
        self.create_zip = create_zip
        self.test = test
        self.platform_data = self.get_platform_data()

        if execute_build_on_init:
            self.execute_builds()

    def get_platform_data(self):
        data = {}
        if self.windows_build_name is not None:
            data.update({Platforms.WINDOWS: Data.template_platform_data[Platforms.WINDOWS].copy()})
        if self.macosx_build_name is not None:
            data.update({Platforms.MACOSX: Data.template_platform_data[Platforms.MACOSX].copy()})
        if self.linux_build_name is not None:
            data.update({Platforms.LINUX: Data.template_platform_data[Platforms.LINUX].copy()})
        return data

    def get_build_name(self, platform):
        if platform == Platforms.WINDOWS:
            return self.windows_build_name
        elif platform == Platforms.MACOSX:
            return self.macosx_build_name
        elif platform == Platforms.LINUX:
            return self.linux_build_name
        else:
            return None

    def package_macosx_build(self, platform_file_path, platform_folder_path):
        extracted_folder_path = Path("{}/{}.app".format(platform_folder_path, self.game_name))
        file_extract_paths = {
            "Info.plist": Path("{}/Contents/Info.plist".format(extracted_folder_path)),
            "PkgInfo": Path("{}/Contents/PkgInfo".format(extracted_folder_path)),
            self.game_name: Path("{}/Contents/MacOS/{}".format(extracted_folder_path, self.game_name)),
            "icon.icns": Path("{}/Contents/Resources/icon.icns".format(extracted_folder_path)),
            "{}.pck".format(self.game_name): Path(
                                                "{}/Contents/Resources/{}.pck".format(
                                                                                    extracted_folder_path,
                                                                                    self.game_name
                                                                                )
                                            )
        }
        self.file_helper.extract_all_zip(zip_src_path=platform_file_path, extract_path=platform_folder_path)
        for file in file_extract_paths:
            src_file_path = file_extract_paths[file]
            dest_file_path = Path("{}/{}".format(platform_folder_path, file))
            self.file_helper.move_file(src_file_path, dest_file_path)
        self.file_helper.remove_file(platform_file_path)
        self.file_helper.remove_directory(extracted_folder_path)

    def execute_builds(self):
        prev_cwd = os.getcwd()
        os.chdir(self.project_path)

        for build_platform in self.platform_data:
            build = self.platform_data[build_platform]
            platform = build[Data.PLATFORM]
            file_ext = build[Data.FILE_EXT]
            platform_folder_name = "{}_{}".format(self.game_name, platform)
            platform_folder_path = Path("{}/{}/{}".format(self.build_path, self.game_name, platform_folder_name))
            platform_file_path = Path("{}/{}{}".format(platform_folder_path, self.game_name, file_ext))
            build_name = self.get_build_name(platform)
            export_flag = "--export"
            if self.export_debug:
                export_flag = "--export-debug"
            export_command = "{} {} \"{}\" {}".format(
                    self.godot_file_path, export_flag, build_name, platform_file_path,
                )

            # print("Initializing build:")
            # print(
            #     json.dumps(
            #         {
            #             "platform": platform,
            #             "file_ext": file_ext,
            #             "platform_folder_name": platform_folder_name,
            #             "platform_folder_path": str(platform_folder_path),
            #             "platform_file_path": str(platform_file_path),
            #             "build_name": build_name,
            #             "export_flag": export_flag,
            #             "export_command": export_command
            #         },
            #         indent=4,
            #         sort_keys=True
            #     )
            # )

            if not self.test:
                # print("Recreating platform build folder at {}".format(platform_folder_path))
                self.file_helper.recreate_directory(platform_folder_path)

                # print("Kicking of build with export command: {}".format(export_command))
                os.system(export_command)

                if build_platform == Platforms.MACOSX:
                    self.package_macosx_build(platform_file_path, platform_folder_path)

                if self.create_zip:
                    self.file_helper.create_zip(
                        "{}/{}.zip".format(self.build_path, platform_folder_name),
                        platform_folder_name,
                        platform_folder_path
                    )

        os.chdir(prev_cwd)
        return self.SUCCESS
