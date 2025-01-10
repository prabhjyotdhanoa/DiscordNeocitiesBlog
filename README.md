Check out my blog at prabd.com/blog
(It uses this program!)

So here's the general idea.
I made a discord bot in Python that runs on my local computer and invited it to my personal server,
It only reacts to messages in the "blog" text channel
Then, it reads the first 2 lines of the message
The first line is the title, and the second line is the tag of the post
To generate some random URL so i can refer to an individual entry, I put the title into a hash function and make that the entry id
Then, the bot edits a local copy of my blog.html on my computer, such that it appends to the top of the blog section
Then, using the neocities API, I upload the file on my desktop to my site.

Notes:
Please don't forget to make a .env file, where inside of it you set the following variables:
# .env
DISCORD_TOKEN="discord token here"
PASSWORD="neocities pw here"
BLOG_PATH="local copy of your blog"
