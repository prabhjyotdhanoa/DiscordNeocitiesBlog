# bot.py
import os
import discord
import hashlib
from neocities import NeoCities
from datetime import datetime

from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
PASSWORD = os.getenv('PASSWORD')

nc = NeoCities('prabd', PASSWORD)

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')
    for guild in client.guilds:
         print(
        f'{client.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})'
        )

@client.event
async def on_message(message):
    # Ignore messages from the bot itself
    if message.author == client.user:
        return
        
    # Check if message is in the blog channel
    if message.channel.name == "blog":
        # Split message into lines
        lines = message.content.split('\n')
        
        if len(lines) < 2:
            await message.channel.send("Please provide a title and tag for your blog post.")
            return
        # Get title from first line
        title = lines[0]
        #Get tag from second line
        tag_line = lines[1]
        
        # Create hash of title for id
        title_hash = hashlib.md5(title.encode()).hexdigest()
        
        # Get current date
        current_date = datetime.now().strftime("%Y-%m-%d")
        
        # Get message content excluding title and tag, and format it as preformatted text
        content = '\n'.join(lines[2:]).replace('<', '&lt;').replace('>', '&gt;')
        
        # Create HTML content
        html_content = f'''            
        <div class="blog-entry" id="{title_hash}">
            <h2><a href="#{title_hash}">{title}</a></h2>
            <p class="meta">Tag: <span>{tag_line}</span> | Date: <span>{current_date}</span></p>
            <pre>{content}</pre>'''
            
        # Add any attached images to the HTML content
        if message.attachments:
            for attachment in message.attachments:
                if attachment.content_type.startswith('image/'):
                    html_content += f'''
            <img src="{attachment.url}" alt="Attached image" style="max-width: 100%;">'''
                    
        html_content += '\n        </div>'
            
        # Send the HTML formatted message back to the channel
        await message.channel.send(f"```html\n{html_content}\n```")
        
        # Append the blog post to blog.html
        blog_file_path = os.getenv('BLOG_PATH')
        with open(blog_file_path, 'r', encoding='utf-8') as file:
            content = file.read()
            
        # Find the append marker and insert the new blog post
        append_marker = "<!-- APPEND HERE -->"
        new_content = content.replace(append_marker, f"{append_marker}\n{html_content}")
        
        # Save the updated content back to the file
        with open(blog_file_path, 'w', encoding='utf-8') as file:
            file.write(new_content)

        # Upload the updated file using Neocities API
        os.chdir("D:/neocities-prabd")
        nc.upload(('blog.html', blog_file_path))
        print("Blog uploaded")

client.run(TOKEN)