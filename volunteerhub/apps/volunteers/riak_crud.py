import riak
import uuid

# For regular HTTP...
# client = riak.RiakClient()

# For Protocol Buffers (go faster!)
client = riak.RiakClient(port=10018, transport_class=riak.RiakPbcTransport)

artifact_bucket = client.bucket('artifact')


def create_artifact(artifact_dict):
    # ``artifact_dict`` should look something like:
    # {
    #     'title': 'Bangor Fire House circa 1908',
    #     'description': 'A description of our bold artifact',
    #     'slug': 'bangor-fire-house-circa-1908',
    #     'address': '102 Broadway Street',
    #     'city': 'Bangor',
    #     'state': 'Maine',
    #     'zipcode': '04401',
    #     'image': 'path/to/image.jpg'
    #     'created': time.time(),
    #     'updated': time.time(),
    #     'created_by': 'username',
    # }
    artifact = artifact_bucket.new(artifact_dict['slug'], data=artifact_dict)
    artifact.store()

def get_artifact(artifact_slug):
    artifact = artifact_bucket.get(artifact_slug)
    return {
        'artifact': artifact.get_data(),
    }


'''
def create_comment(entry_slug, comment_dict):
    # ``comment_dict`` should look something like:
    # {
    #     'author': 'Daniel',
    #     'url': 'http://pragmaticbadger.com/',
    #     'posted': time.time(),
    #     'content': 'IS IT WEBSCALE? I HEARD /DEV/NULL IS WEBSCALE.',
    # }
    # Error handling omitted for brevity...
    entry = artifact_bucket.get(entry_slug)

    # Give it a UUID for the key.
    comment = comment_bucket.new(str(uuid.uuid1()), data=comment_dict)
    comment.store()

    # Add the link.
    entry.add_link(comment)
    entry.store()
'''

'''
def get_entry_and_comments(entry_slug):
    entry = artifact_bucket.get(entry_slug)
    comments = []

    # They come out in the order you added them, so there's no
    # sorting to be done.
    for comment_link in entry.get_links():
        # Gets the related object, then the data out of it's value.
        comments.append(comment_link.get().get_data())

    return {
        'entry': entry.get_data(),
        'comments': comments,
    }
'''

'''
# To test:
if __name__ == '__main__':
    create_entry({
        'title': 'First Post!',
        'author': 'Daniel',
        'slug': 'first-post',
        'posted': time.time(),
        'tease': 'A test post to my new Riak-powered blog.',
        'content': 'Hmph. The tease kinda said it all...',
    })

    create_comment('first-post', {
        'author': 'Matt',
        'url': 'http://pragmaticbadger.com/',
        'posted': time.time(),
        'content': 'IS IT WEBSCALE? I HEARD /DEV/NULL IS WEBSCALE.',
    })
    create_comment('first-post', {
        'author': 'Daniel',
        'url': 'http://pragmaticbadger.com/',
        'posted': time.time(),
        'content': 'You better believe it!',
    })

    data = get_entry_and_comments('first-post')
    print "Entry:"
    print data['entry']['title']
    print data['entry']['tease']
    print
    print "Comments:"

    for comment in data['comments']:
        print "%s - %s" % (comment['author'], comment['content'])
'''