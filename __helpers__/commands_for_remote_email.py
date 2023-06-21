#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 24 18:08:28 2023

@author: dale
"""


from fabric import Connection
from pathlib import Path
import sys

if str(Path(__file__).parent) not in sys.path:
    sys.path.append(str(Path(__file__).parent))
from __helpers__.compose_email import ComposeEmail



def trasfer_file_to_remote(
        conn: Connection,
        file_path: str,
        save_path: str) -> None:
    with conn:
        conn.put(file_path, save_path)


def run_remote_command_in_shell(
        conn: Connection,
        command_str: str) -> None:
    with conn:
        conn.run(command_str, asynchronous=False)


def create_send_email_commands(
        html_path: str,
        csv_or_excel_path: str,
        *,
        png_path: str=None,
        pdf_path: str=None,) -> tuple:
    main_dir = ComposeEmail._vm_email_path  # this needs to match remote box
    html_dir = Path(main_dir, 'html_files')
    html_path = Path(html_dir, Path(html_path).name)
    csv_dir = Path(main_dir, 'email_lists')
    csv_or_excel_path = Path(csv_dir, Path(csv_or_excel_path).name)
    
    command_activate_venv_command = " ".join(
        [
            'source',
            f'{str(main_dir)}/venv/bin/activate'
         ]
    )
    command_send_html_email = [
        'python3.11',
        f'"{str(main_dir)}/__helpers__/compose_email.py"',
        f'"{str(html_path)}"',
        f'"{str(csv_or_excel_path)}"',
    ]
        
    command_clear_folders = [
        'rm',
        f'"{str(html_path)}"',
        '&&',
        'rm',
        f'"{str(csv_or_excel_path)}"'
    ]

    if png_path:
        png_dir = Path(main_dir, 'email_png')
        png_path = Path(png_dir, Path(png_path).name)
        send_command = [
            '--png_path'
            f' "{str(png_path)}"'
        ]
        clear_command = [
            '&&',
            'rm',
            f'"{str(png_path)}"'
        ]
        command_send_html_email = command_send_html_email + send_command
        command_clear_folders = command_clear_folders + clear_command
        
    if pdf_path:
        pdf_dir = Path(main_dir, 'pdf_attach')
        pdf_path = Path(pdf_dir, Path(pdf_path).name)
        send_command = [
            '--pdf_path'
            f' "{str(pdf_path)}"'
        ]
        clear_command = [
            '&&',
            'rm',
            f'"{str(pdf_path)}"'
        ]
        command_send_html_email = command_send_html_email + send_command
        command_clear_folders = command_clear_folders + clear_command
    command_send_html_email_str = " ".join(command_send_html_email)
    command_clear_folders_str = " ".join(command_clear_folders)
    return (
        command_activate_venv_command,
        command_send_html_email_str,
        command_clear_folders_str,

    )

if __name__ == '__main__':
    vm_command = create_send_email_commands(
        'test-path.html',
        'test-path.csv',
        png_path='test-path.png',
        pdf_path='test-path.pdf'
        )
    print(vm_command)