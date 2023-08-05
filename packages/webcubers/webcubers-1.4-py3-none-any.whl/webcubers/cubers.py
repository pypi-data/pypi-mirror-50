#!/usr/bin/env python3

from webcubers import WebCubers
import argparse
import sys
import appdirs
import os
import sys
import cutie

def banner():
    print(f'''
 __    __     _       ___      _                   
/ / /\ \ \___| |__   / __\   _| |__   ___ _ __ ___ 
\ \/  \/ / _ \ '_ \ / / | | | | '_ \ / _ \ '__/ __|
 \  /\  /  __/ |_) / /__| |_| | |_) |  __/ |  \__ \\
  \/  \/ \___|_.__/\____/\__,_|_.__/ \___|_|  |___/
              < WebCubers-CLI v{WebCubers.module_version} >
''')

def login(username=None, api_key=None):
    if username:
        webcubers = WebCubers(username, api_key)
        if webcubers.is_authenticated:
            with open(session_path, 'w+') as session_file:
                session_file.write(f'{username},{api_key}')
            return True
        else:
            return webcubers.error
    else:
        if not os.path.exists(session_path):
            print('[-] Session not found please login again.')
            sys.exit()
        else:
            with open(session_path, 'r') as session_file:
                username, api_key = str(session_file.read()).split(',')
            webcubers = WebCubers(username, api_key)
            if webcubers.is_authenticated:
                return webcubers
            else:
                print(f'[-] {webcubers.error}')
                sys.exit()

def logout():
    try:
        os.remove(session_path)
        return True
    except:
        return False

def download_snippet(snippet_id):
    webcubers = login()
    snippet = webcubers.snippet(snippet_id)
    try:
        snippet_filename = snippet['data']['filename']
        if snippet['status']:
            with open(snippet_filename, 'w') as snippet_file:
                snippet_file.write(snippet['data']['code'])
            print(f'[+] Snippet {snippet_filename} created successfully.')
        else:
            print(f'[-] {snippet["message"]}')
    except :
        print(f'[-] {snippet["message"]}')


def arg_logout(args):
    try_logout = logout()
    if try_logout == True:
        print('[+] You have successfully signed out.')
    else:
        print(f'[-] Problem occurred with removing session, please try login again.')

def arg_profile(args):
    webcubers = login()
    profile = webcubers.profile()
    if profile['status'] == True:
        print('[+] Profile information :\n')
        for profile_key, profile_value in profile['data'].items():
            print(f'\t[+] {profile_key} : {profile_value}')
    else:
        print(f'[-] Problem occurred with removing session, please try login again.')

def arg_login(args):
    try_login = login(args.username, args.api_key)
    if try_login == True:
        print('[+] You have successfully signed in webcubers.')
    else:
        print(f'[-] {try_login}')

def arg_snippets(args):
    webcubers = login()
    snippets = webcubers.snippets()

    snippets_ids = []
    snippets_info = []
    for snippet in snippets['data']:
        snippets_info.append(f'{snippet["filename"]} ( {snippet["title"]} )')
        snippets_ids.append(f'{snippet["id"]}')
    
    print('Select snippet to download :')
    target_snippet_id = cutie.select(
        snippets_info,
        deselected_prefix='\t',
        selected_prefix='\t => ')

    download_snippet(snippets_ids[target_snippet_id])

def main():
    global session_path, app_path
    banner()

    app_path = appdirs.user_data_dir('Cubers','WebCubers')
    session_path = os.path.join(app_path, 'session')

    if not os.path.exists(app_path):
        os.makedirs(app_path)
    
    # parser
    cli_parser = argparse.ArgumentParser(prog='cubers', description='WebCubers CLI Connector.')
    cli_subparsers = cli_parser.add_subparsers()

    login_command = cli_subparsers.add_parser('login')
    login_command.add_argument('username')
    login_command.add_argument('api_key')
    login_command.set_defaults(func=arg_login)

    snippets_command = cli_subparsers.add_parser('snippets')
    snippets_command.set_defaults(func=arg_snippets)

    logout_command = cli_subparsers.add_parser('logout')
    logout_command.set_defaults(func=arg_logout)

    profile_command = cli_subparsers.add_parser('profile')
    profile_command.set_defaults(func=arg_profile)

    if len(sys.argv) <= 1:
        sys.argv.append('--help')

    # Execute parse_args()
    args = cli_parser.parse_args()
    args.func(args)

if __name__ == '__main__':
    main()