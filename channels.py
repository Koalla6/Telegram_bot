from ez_telegram import EzClient
from database import russian_channels, ukrainian_channels, ukrainian_channels_r


def channels_rus(word_list):
    count = 0
    client = EzClient()
    russian_links = russian_channels()
    for i in russian_links:
        # print("\n", i)
        try:
            message = client.get_messages(channel=i)
            for i in word_list:
                # print(i)
                filter_object = filter(lambda a: i in a, message)
                # print("here")
                if list(filter_object) != []:
                    # print(i, "True")
                    count += 1
        except:
            print("Exception found")
            continue
    percents = 100 * count / (len(russian_links) * len(word_list))
    return percents


def channels_ukr(word_list):
    count = 0
    client = EzClient()
    ukrainian_links = ukrainian_channels()
    for i in ukrainian_links:
        try:
            message = client.get_messages(channel=i)
            for i in word_list:
                filter_object = filter(lambda a: i in a, message)
                if list(filter_object) != []:
                    count += 1
        except:
            print("Exception found")
            continue
    percents = 100 * count / (len(ukrainian_links) * len(word_list))
    return percents


def channels_ukr_r(word_list):
    count = 0
    client = EzClient()
    ukrainian_links_r = ukrainian_channels_r()
    for i in ukrainian_links_r:
        try:
            message = client.get_messages(channel=i)
            for i in word_list:
                filter_object = filter(lambda a: i in a, message)
                if list(filter_object) != []:
                    count += 1
        except:
            print("Exception found")
            continue
    percents = 100 * count / (len(ukrainian_links_r) * len(word_list))
    return percents

# message = client.get_messages(channel="VARTA1")


# client = EzClient()
# message = client.get_messages(channel="rian_ru")
# filter_object = filter(lambda a: "СССР" in a, message)
# if list(filter_object) != []:
#     print("True")
# else:
#     print("False")


# list(map(print, message))

# for i in message:
#     if i

# test_list = []
# #
#     for i in word_list:
# #print(i)
#     filter_object = filter(lambda a: i in a, message)
#     #print("here")
#     if list(filter_object) != []:
#         print(i, "True")
#     else:
#         print(i, "False")
# print("\t\t here \t", message)


# #list(map(print, filter_object))
# print(list(filter_object))

# print(message)
# list = ["gyh", "jfn", "frhuj"]
# print(list)
