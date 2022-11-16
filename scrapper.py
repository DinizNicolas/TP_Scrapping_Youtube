import sys
import json
import requests
from bs4 import BeautifulSoup

def get_links(filejson):
    links = []
    path = None
    #In the json tree, sometimes there is a list instead of a dictionnary. These list are not always in the same order
    #The next two for loops are there to find the correct dictionnary in the list
    for i in range(len(filejson["engagementPanels"])):
        if "structuredDescriptionContentRenderer" in filejson["engagementPanels"][i]["engagementPanelSectionListRenderer"]["content"]:
            path = filejson["engagementPanels"][i]["engagementPanelSectionListRenderer"]["content"]
            break
    if path:
        for i in range(len(path["structuredDescriptionContentRenderer"]["items"])):
            if "expandableVideoDescriptionBodyRenderer" in path["structuredDescriptionContentRenderer"]["items"][i]:
                path = path["structuredDescriptionContentRenderer"]["items"][i]
                break

    #If a path was found, the links are retrieved
    if path:
        data = path["expandableVideoDescriptionBodyRenderer"]["descriptionBodyText"]["runs"]
    
        for elem in data:
            if "navigationEndpoint" in elem:
                #Possibility to get more information about each link in "elem"
                links.append(elem["text"])

    return links

def get_likes(filejson):
    try:
        data = filejson["contents"]["twoColumnWatchNextResults"]["results"]["results"]["contents"][0]["videoPrimaryInfoRenderer"]["videoActions"]["menuRenderer"]["topLevelButtons"][0]["segmentedLikeDislikeButtonRenderer"]["likeButton"]["toggleButtonRenderer"]["defaultText"]["accessibility"]["accessibilityData"]["label"]
        out = ''.join( [x for x in data if x.isnumeric()])
    except:
        print("There is no like")
        out = None

    return out

def get_comments(filejson):
    try:
        data = filejson["contents"]["twoColumnWatchNextResults"]["results"]["results"]["contents"][2]["itemSectionRenderer"]["contents"][0]["commentsEntryPointHeaderRenderer"]["contentRenderer"]["commentsEntryPointTeaserRenderer"]["teaserContent"]["simpleText"]
    except:
        print("There is no comment")
        data = None

    return [data]

def get_js_var_json(var_name,soup):
    string_ = "var "+var_name
    #Search for a javascript variable in script tags
    #If found, extract the dictionnary from the variable
    for data_tmp in soup.find_all("script"):
        if string_ in str(data_tmp):
            tmp = str(data_tmp).split('};')[0].split(string_+" = ")[1]
            return json.loads(tmp+"}")
    return None

def get_html_from_id(id):
    url = "https://www.youtube.com/watch?v=" + id
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    return soup

def checking_arguments(files_names,list_args,N_ARGS):
    #Correct number of argument
    if len(list_args) != 2*N_ARGS+1:
        sys.exit('Incorrect number of arguments')
    #Correct type of argument
    for key in files_names:
        if key not in list_args:
            sys.exit('Input not found: '+key)

    return 0

def generate_dict_from_id(id):
    output_data = {"title":None,"author":None,"likes":None,"description":None,"links":[],"id":None,"comments":[]}

    soup = get_html_from_id(id)

    output_data["id"] = id
    output_data["author"] = soup.find("link", itemprop="name").get("content")

    tmp_json = get_js_var_json("ytInitialPlayerResponse",soup)
    output_data["title"] = tmp_json["videoDetails"]["title"]
    output_data["description"] = tmp_json["videoDetails"]["shortDescription"]

    tmp_json = get_js_var_json("ytInitialData",soup)
    output_data["links"] = get_links(tmp_json)
    output_data["likes"] = get_likes(tmp_json)
    output_data["comments"] = get_comments(tmp_json)

    return output_data

def load_json(file_name):
    file = open(file_name, 'r')
    data_input = json.load(file)
    file.close()
    return data_input

if __name__ == '__main__':

    files_names = {"--input":None,"--output":None}
    N_ARGS = 2

    list_args = sys.argv
    #Checking if user inputs are correct
    checking_arguments(files_names,list_args,N_ARGS)

    #Retrieving arguments
    for i in range(1,2*N_ARGS,2):
        files_names[list_args[i]] = list_args[i+1]

    #Open and load JSON file
    data_input = load_json(files_names['--input'])

    output_dict = {}
    for id in data_input['videos_id']:
        print("Scrapping "+id)
        output_dict[id] = generate_dict_from_id(id)


    #Write output in JSON file
    with open(files_names['--output'], 'w', encoding='utf-8') as file:
        json.dump(output_dict, file, ensure_ascii=False)