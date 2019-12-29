import PIL
from PIL import Image
import urllib.request
import io,sys,random,math
def distance(list1,list2):
    return (list1[0]-list2[0])**2 + (list1[1]-list2[1])**2 + (list1[2]-list2[2])**2

def main():
    URL = sys.argv[2] #https://cf.geekdo-images.com/imagepage/img/5lvEWGGTqWDFmJq_MaZvVD3sPuM=/fit-in/900x600/filters:no_upscale()/pic260745.jpg
    K = int(sys.argv[1])
    f = io.BytesIO(urllib.request.urlopen(URL).read())
    img = Image.open(f)
    img = img.show()
    img = Image.open(f)
    pix = img.load()
    centroids = []
    cent = []
    lengths = []
    oldLengths = []
    countDiff = 0
    condition = True
    print("Size: " + str(img.size[0]) + " x "+ str(img.size[1]))
    print("Pixels: "+str(img.size[0]*img.size[1]))
    dictDistinct = {}
    listDistinct = []
    for e in range(img.size[0]):
        for r in range(img.size[1]):
            if pix[e,r] not in dictDistinct.keys():
                dictDistinct[pix[e,r]] = 1
            else:
                dictDistinct[pix[e,r]] = dictDistinct[pix[e,r]]+1
            listDistinct.append(pix[e,r])
    print("Distinct pixel count: " + str(len(dictDistinct.keys())))
    mostCommon = max(dictDistinct,key = dictDistinct.get)
    print("Most common pixel: " + str(mostCommon) + " => " + str(dictDistinct[mostCommon]))
    for i in range(K):
        x = random.randint(0,img.size[0])
        y = random.randint(0,img.size[1])
        centroids.append([pix[x,y]])
        cent.append(pix[x,y])
    print("Random Means:",cent)
    while True:
        lengths = []
        pixTrack = []
        for i in range(K):
            lengths.append(0)
            pixTrack.append([])
        for j in range(img.size[0]):
            for k in range(img.size[1]):
                distances = []
                for l in range(K):
                    distances.append(distance(centroids[l][0],pix[j,k]))
                minimum = min(distances)
                index = distances.index(minimum)
                centroids[index].append(pix[j,k])
                pixTrack[index].append((j,k))
                lengths[index] = lengths[index]+1
        if len(oldLengths) == 0:
            print("Starting Sizes:",lengths)
            oldLengths = lengths
        else:
            delta = []
            countDiff+=1
            for ind in range(0,len(oldLengths)): delta.append(lengths[ind]-oldLengths[ind])
            oldLengths = lengths
            #print("Diff 1:", delta)
            if delta.count(0) == len(delta): condition = False
        newCentroids = []
        for i in range(len(centroids)):
            sumr = 0
            sumg = 0
            sumb = 0
            for j in range(len(centroids[i])):
                sumr+=centroids[i][j][0]
                sumg+=centroids[i][j][1]
                sumb+=centroids[i][j][2]
            newCentroids.append([[sumr/len(centroids[i]),sumg/len(centroids[i]),sumb/len(centroids[i])]])
        centroids = newCentroids
        if condition == False: break
    ct = 1
    print("Final means:")
    #print("finalrgb", centroids)
    for q in range(len(pixTrack)):
        for w in range(len(pixTrack[q])):
            pixel = pixTrack[q][w]
            pix[pixel[0],pixel[1]] = (int(centroids[q][0][0]),int(centroids[q][0][1]),int(centroids[q][0][2]))
    dictDist = {}
    for e in range(img.size[0]):
        for r in range(img.size[1]):
            if pix[e,r] not in dictDist.keys():
                dictDist[pix[e,r]] = 1
            else:
                dictDist[pix[e,r]] = dictDist[pix[e,r]]+1
    for t in range(len(centroids)):
        print(str(ct)+": "+str(tuple(centroids[t][0]))+" => "+str(dictDist[(int(centroids[t][0][0]),int(centroids[t][0][1]),int(centroids[t][0][2]))]))
        ct+=1
    print("Region counts: ", 0)
    img.show()
    img.save("kmeans/{}.png".format("2021dhan"),"PNG")

if __name__ == '__main__':
    main()
