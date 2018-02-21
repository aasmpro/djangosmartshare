def readable_size(size, label):
    size_replace = {
        'Byte': 'KB',
        'KB': 'MB',
        'MB': 'GB'
    }
    if size >= 1024 and label != 'GB':
        size /= 1024
        label = size_replace[label]
        readable_size(size, label)

    return '{} {}'.format(size, label)


print(readable_size(2458, 'Byte'))
