require 'kramdown'

if ARGV.length != 2
  puts "usage: ruby script.rb <input_file> <output_file>"
  exit(1)
end

# get paths from terminal
input_file = ARGV[0]
output_file = ARGV[1]

unless File.exist?(input_file)
  puts "error: '#{input_file}' non-existed!"
  exit(1)
end

# from Markdown to HTML
begin
  markdown_content = File.read(input_file)
  html_content = Kramdown::Document.new(markdown_content).to_html
  File.write(output_file, html_content)
  puts "Success: '#{input_file}' -> '#{output_file}'"
rescue => e
  puts "Error: #{e.message}"
end
