@echo off
if "%~1"=="" (
    echo md_to_html.bat [input_path]
    exit /b 1
)

set input_file=%~1
set output_file=%~n1.html

ruby C:\D\bat_script\md_to_html.rb "%input_file%" "%output_file%"

python C:\D\bat_script\md_to_page.py "%output_file%"

exit /b 0
