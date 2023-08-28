import os
import urllib.request
import subprocess
import shutil
from os.path import expandvars
import ctypes  # For the pop-up

def install_game():
    # PART 1: INSTALLATION
    # Define URLs and paths
    steamcmd_url = "https://steamcdn-a.akamaihd.net/client/installer/steamcmd.zip"
    steamcmd_zip = "steamcmd.zip"
    steamcmd_extract_path = "C:/steamcmd"  # Install SteamCMD to C drive
    game_install_path = "C:/icarus"  # Install the game to C:\icarus
    game_app_id = "2089300"  # Provided game App ID (Icarus)

    # Download SteamCMD
    urllib.request.urlretrieve(steamcmd_url, steamcmd_zip)

    # Extract SteamCMD
    os.makedirs(steamcmd_extract_path, exist_ok=True)
    subprocess.run(["powershell", "Expand-Archive", steamcmd_zip, steamcmd_extract_path], check=True)

    # Install the game using SteamCMD
    steamcmd_path = os.path.join(steamcmd_extract_path, "steamcmd.exe")
    game_install_command = [
        steamcmd_path,
        "+login", "anonymous",
        "+force_install_dir", os.path.join(game_install_path, "steamapps", "common"),
        "+app_update", game_app_id,
        "+quit"
    ]
    subprocess.run(game_install_command, shell=True, check=True)

    print("Game installation completed.")


def create_batch_file():
    # Create the batch file on the desktop
    batch_script = """
    @echo off
    start C:\icarus\steamapps\common\icarusserver.exe -log
    """

    desktop_path = os.path.join(os.environ["USERPROFILE"], "Desktop")
    batch_file_path = os.path.join(desktop_path, "run_server.bat")
    with open(batch_file_path, "w") as batch_file:
        batch_file.write(batch_script)

    print("Batch file created on the desktop.")


# PART 2: FILE HANDLING
# Set the base path to the directory
def handle_files():
    # Define the folder structure
    folders_to_create = [
        "c:\\Icarus\\steamapps\\common\\Icarus\\Saved\\Config\\WindowsServer",
        "c:\\Icarus\\steamapps\\common\\Icarus\\Saved\\PlayerData\\DedicatedServer\\Prospects"
    ]

    # Create the folders
    for folder_path in folders_to_create:
        os.makedirs(folder_path, exist_ok=True)

    base_path = expandvars(r'%UserProfile%\AppData\Local\Icarus\Saved\PlayerData')

    # Find the first folder in the base directory
    for folder_name in os.listdir(base_path):
        folder_path = os.path.join(base_path, folder_name)
        if os.path.isdir(folder_path):
            your_steam_id_number = folder_name
            break

    # Construct the source folder path
    source_folder_path = os.path.join(base_path, your_steam_id_number, 'Prospects')

    # Ask the user for the source file name
    source_file_name = input('Enter the source file name (ProspectName.json): ')
    source_file_path = os.path.join(source_folder_path, source_file_name + '.json')

    # Check if the source file exists
    if not os.path.exists(source_file_path):
        print('Source file does not exist.')
    else:
        # Backup the source file
        backup_file_path = os.path.join(source_folder_path, f'backup_{source_file_name}.json')
        shutil.copy(source_file_path, backup_file_path)
        print(f'Backup of {source_file_name}.json created.')

        # Construct the destination folder path
        destination_path = "c:\\Icarus\\steamapps\\common\\Icarus\\Saved\\PlayerData\\DedicatedServer\\Prospects"

        # Copy the source file to the destination folder
        shutil.copy(source_file_path, os.path.join(destination_path, f'{source_file_name}.json'))

        print('File copied to destination folder.')

        # Define the content for the SystemSettings.ini file
        system_settings_content = f"""
        [/Script/Icarus.DedicatedServerSettings]
        SessionName=
        JoinPassword=
        MaxPlayers=
        AdminPassword=
        ShutdownIfNotJoinedFor=300.000000
        ShutdownIfEmptyFor=300.000000
        AllowNonAdminsToLaunchProspects=True
        AllowNonAdminsToDeleteProspects=False
        LoadProspect=
        CreateProspect=
        ResumeProspect=True
        LastProspectName={source_file_name}
        """

        # Define the path to the SystemSettings.ini file
        system_settings_file_path = "c:\\Icarus\\steamapps\\common\\Icarus\\Saved\\Config\\WindowsServer\\SystemSettings.ini"

        # Write the content to the SystemSettings.ini file
        with open(system_settings_file_path, "w") as file:
            file.write(system_settings_content)

        print('File copied to destination folder and settings updated.')
def main():
    while True:  # Keep showing the menu
        print("1. Install Game")
        print("2. Create Batch File")
        print("3. Handle Files")
        print("4. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            install_game()
        elif choice == "2":
            create_batch_file()
        elif choice == "3":
            handle_files()
        elif choice == "4":
            print("Exiting.")
            input("Press Enter to close...")
            break  # Exit the while loop
        else:
            print("Invalid choice.")

        # Display the dialog box with the message "Task Completed"
        ctypes.windll.user32.MessageBoxW(0, "Task Completed. Please check the console for details.", "Task Complete", 1)

if __name__ == "__main__":
    main()
