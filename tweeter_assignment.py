# Import dpendencies
import tweepy


def download_followers(api):
    # get the user
    user = api.get_user(api.me().screen_name)

    # get the followers of user
    user_followers = user.followers()
    # create a user_followers list which will store all the user
    user_followers_list = []

    # Open a file user_followers
    file1 = open("users_followers_list.txt", "w")

    # Loop over all the followers object and extract the followers screen name/ user name
    for followers in user_followers:
        user_followers_list.append(
            [followers.id, followers.screen_name, followers.followers_count, followers.friends_count])

        file1.write(followers.screen_name + " \n")

    # Close
    file1.close()
    return user_followers_list


def rank_user_followers(user_followers_list):
    # custom functions to rank user_friends_list
    def get_name(follower):
        return follower[1]

    def get_follower_followers_count(follower):
        return follower[2]

    def get_follower_friends_count(follower):
        return follower[3]

    # sort by name (Ascending order)
    user_followers_list.sort(key=get_name)
    print("Rank by name (Ascending order)")
    print(user_followers_list, end='\n\n')

    # sort by follower_followers_count (Ascending order)
    user_followers_list.sort(key=get_follower_followers_count)
    print("Rank by followers_count (Ascending order)")
    print(user_followers_list, end='\n\n')

    # sort by friends_count (Descending order)
    user_followers_list.sort(key=get_follower_friends_count, reverse=True)
    print("Rank by friends_count (Descending order)")
    print(user_followers_list, end='\n\n')


def send_DM(api, followers_id):
    # take text_message input from user
    # this message will be send to all the followers
    text_message = input("Please write a message you want to send: ")
    send_message_status_id_list = []

    # loop over the follower_id and send text_message
    # append the send message status_id
    # this status_id can be used to delete the send_message
    for id in followers_id:
        status = api.send_direct_message(id, text_message)
        send_message_status_id_list.append(status.id)

    # delete the send messahe
    for id in send_message_status_id_list:
        api.destroy_direct_message(id)
    print("Send message deleted")


def main():
    # We will take apli key and api consumer_key and api consumer_secret
    # auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    # auth.set_access_token(access_token, access_token_secret)
    consumer_key = input("Please enter the Twitter API consumber_key : ")
    consumer_secret = input("Please enter the Twitter API consumber_secret : ")

    access_token = input("Please enter the Twitter API access_token : ")
    access_token_secret = input(
        "Please enter the Twitter API access_token_secret : ")

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    api = tweepy.API(auth)

    # Download the the user followers and return a user_friends_list
    # user_friends_list willcontain the screen_name, followers_count and friends_count
    # We will use this user_friends_list to sort based on some creteria
    user_followers_list = download_followers(api)

    # rank the user_friends_list
    rank_user_followers(user_followers_list)

    # extract the followers_id
    followers_id = []
    for follower in user_followers_list:
        followers_id.append(follower[0])
    # print(followers_id)

    send_DM(api, followers_id)


if __name__ == "__main__":
    main()
