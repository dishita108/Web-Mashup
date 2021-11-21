from django.shortcuts import render
import Algorithmia
import requests,json
import Algorithmia

#happy : https://i1.wp.com/www.studica.com/blog/storage/2013/01/Smiling-Woman.jpg?fit=300%2C200&ssl=1
#angry : https://i.pinimg.com/originals/9b/76/6b/9b766b7c8b51fd6545ab1c68ed5bad4a.jpg

def render_gif(emotion):
    apikey = "JHGPQW"  # test value
    lmt = 3

    # our test search
    search_term = emotion

    # get the top 8 GIFs for the search term using default locale of EN_US
    r = requests.get(
        "https://g.tenor.com/v1/search?q=%s&key=%s&limit=%s" % (search_term, apikey, lmt))

    if r.status_code == 200:
        # load the GIFs using the urls for the smaller GIF sizes
        #top_8gifs = json.loads(r.content)
        url_list=[]
        img_list=[]
        top_8gifs= r.json()
        print (top_8gifs)
        print("\n\n\n")
        print("Recommended gifs : \n")
        for i in range(lmt):
            print(top_8gifs['results'][i]['url'])
            url_list.append(top_8gifs['results'][i]['url'])

    else:
        top_8gifs = None
    return(url_list)
# Create your views here.
def getEmotion(request):
    if request.POST:
        i_url = request.POST['i_url']
        print(i_url)

        client = Algorithmia.client("simDs+9Z3hROfDZAfL")

        input = {
            "image": i_url,
            "numResults": 7
        }

        algo = client.algo('deeplearning/EmotionRecognitionCNNMBP/0.1.2')

        result = algo.pipe(input).result
        emotion = result['results'][0][1]
        print("\nResponse from Algorithmia Emotion API : ")
        print(result)
        print("\n\nEmotion Detected :")
        print(emotion)
        print()
        final = render_gif(emotion)
    return render(request,'index.html',{'emotion':emotion,'url_list':final,'img':i_url})

def home(request):
    return render(request,'index.html')