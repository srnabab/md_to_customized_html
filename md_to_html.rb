require 'kramdown'

# 检查是否提供了正确的命令行参数
if ARGV.length != 2
  puts "用法: ruby script.rb <输入文件> <输出文件>"
  exit(1)
end

# 从命令行参数中获取文件名
input_file = ARGV[0]
output_file = ARGV[1]

# 检查输入文件是否存在
unless File.exist?(input_file)
  puts "错误: 输入文件 '#{input_file}' 不存在!"
  exit(1)
end

# 读取 Markdown 文件并转换为 HTML
begin
  markdown_content = File.read(input_file)
  html_content = Kramdown::Document.new(markdown_content).to_html
  File.write(output_file, html_content)
  puts "转换成功: '#{input_file}' -> '#{output_file}'"
rescue => e
  puts "错误: 转换过程中出现问题: #{e.message}"
end
