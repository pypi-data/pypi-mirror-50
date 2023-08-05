import scrapy
from scrapy.crawler import CrawlerProcess
import textwrap
import os
import json
import media_helper as mediah
import draw_helper as draw
import shutil
import uuid
import text_process
import random
class MSNSpiderSpeaker(scrapy.Spider):
    name = "MSNSpider"
    parent_path="/var/msn"
    bg_sound_path="/var/msn/bg/01.wav"
    outro_path="/var/msn/bg/s45iJEcUZKI.avi"
    output="/var/msn/tmp/x1.avi"
    max_text_read=190
    wrap_text_len=70
    tl="vi"
    def parse(self, response):
        tmp_path = os.path.join(self.parent_path, "tmp")
        font_file = os.path.join(self.parent_path, "fonts/Arial-Unicode-Bold.ttf")
        self.max_text_read=int(self.max_text_read)
        self.wrap_text_len=int(self.wrap_text_len)
        if not os.path.exists(tmp_path):
            os.mkdir(tmp_path)
        arr_imageT = response.xpath('//div[@id="maincontent"]//span/img/@data-src').extract()
        arr_image = []
        for imageT in arr_imageT:
            imgObj = json.loads(imageT)
            src=imgObj['default']['src']
            src=src.split("?")[0] #+"?h=720&w=1280&m=6&q=100&u=t&o=t&l=f&x=640&y=360"
            arr_image.append(mediah.makefullhd("http:"+src,tmp_path))

        arr_text = response.xpath('//div[@id="maincontent"]//p[not (descendant::img or descendant::a)]').extract()
        draw.nomalize_text(arr_text,self.max_text_read)
        draw.balance_image(arr_image, arr_text)
        i=0
        arr_vid=[]
        while(i<len(arr_image)):
            img_source=arr_image[i]
            text_input=arr_text[i]
            if text_input==None or text_input =="":
                soundI = mediah.make_sound_null(6,tmp_path)
            else:
                img_source = draw.content(arr_image[i], text_input,font_file,tmp_path,self.wrap_text_len)
                textTran=";;".join(textwrap.wrap(text_input.replace("\"","\\\""),self.max_text_read))
                soundI = os.popen("php trans.php --tmp=\""+tmp_path+"\" --text=\"" + textTran + "\" --tl="+self.tl).read()
                soundI=mediah.speedup_sound(soundI,tmp_path)
                duration = mediah.duration(soundI)
                if (duration < 1):
                    soundI = mediah.make_sound_null(6,tmp_path)
            arr_vid.append(mediah.makevid(img_source,soundI,tmp_path))
            i+=1
        for img in arr_image:
            try:
                os.remove(img)
            except:
                pass
        if self.outro_path !="None":
            new_outro_path=tmp_path+"/"+uuid.uuid4().hex +".avi"
            shutil.copyfile(self.outro_path, new_outro_path)
            arr_vid.append(new_outro_path)
        mediah.mergvid(arr_vid,tmp_path,self.output)
        #mediah.mix_sound_bg(merged_vid,self.bg_sound_path,tmp_path,self.output)
class MSNSpiderAudioBG(scrapy.Spider):
    name = "MSNSpider"
    parent_path="/var/msn"
    bg_sound_path="/var/msn/bg/01.wav"
    outro_path="/var/msn/bg/s45iJEcUZKI.avi"
    logo_path="UK_Logo.png"
    output="/var/msn/tmp/x1.avi"
    max_text_read=190
    wrap_text_len=70
    lang='en'
    tl="vi"
    part=0
    is_done_part=0
    max_vid_times=20
    def parse(self, response):
        tmp_path = os.path.join(self.parent_path, "tmp")
        font_file = os.path.join(self.parent_path, "fonts/Arial-Unicode-Bold.ttf")
        self.max_text_read=int(self.max_text_read)
        self.wrap_text_len=int(self.wrap_text_len)
        if not os.path.exists(tmp_path):
            os.mkdir(tmp_path)
        arr_imageT = response.xpath('//div[@id="maincontent"]//span/img/@data-src').extract()
        is_photo_news=False
        time_frame=10
        if(len(arr_imageT)==0):
            is_photo_news=True
            time_frame=15
        arr_imageT+= response.xpath('//ul[contains(@class,"slideshow")]/li//img/@data-src').extract()

        if (is_photo_news and len(arr_imageT) > 0):
            infor = {}
            infor['part_done'] = 0
            arr_text = response.xpath('//div[@class="gallerydata"]//div[@class="body-text"]').extract()
            lenImage=len(arr_imageT)
            self.part=int(self.part)
            index=self.part*self.max_vid_times
            if((lenImage-index)//self.max_vid_times >= 2):
                arr_imageT=arr_imageT[index:index+self.max_vid_times]
                arr_text=arr_text[index:index+self.max_vid_times]
            else:
                arr_imageT = arr_imageT[index:]
                arr_text = arr_text[index:]
                self.is_done_part=1
                infor['part_done'] = 1
            self.part += 1
            infor['part'] = self.part
            outputf, ext = os.path.splitext(self.output)
            outputf += ".info"
            with open(outputf, 'w') as outfile:
                json.dump(infor, outfile)
        else:
            arr_text = response.xpath('//div[@id="maincontent"]//p[not (descendant::img or descendant::a)]').extract()

        arr_image = []
        if(len(arr_imageT)>40):
            arr_imageT=arr_imageT[:40]
        for imageT in arr_imageT:
            #print(imageT)
            imgObj = json.loads(imageT)
            try:
                src=imgObj['default']['src']
            except:
                src=imgObj['default']
            src = src.split("?")[0] #+ "?h=720&w=1280&m=6&q=100&u=t&o=t&l=f&x=300&y=0"
            arr_image.append(mediah.makefullhd("http:"+src,tmp_path,self.logo_path))

        title=response.xpath('//title/text()').extract_first().strip()
        if(is_photo_news and not(self.part==1 and self.is_done_part==1)):
            title+=" #"+str(self.part)
        # make logo
        text_process.make_title(title, ' '.join(arr_text),arr_image[random.randint(0,len(arr_image)-1)],
                                font_file,88, self.lang, tmp_path,self.logo_path,self.output)
        if(not is_photo_news):
            draw.nomalize_text(arr_text,self.max_text_read)
        else:
            draw.clean_text(arr_text)
        draw.balance_image(arr_image, arr_text)
        outputCnt, ext = os.path.splitext(self.output)
        outputCnt += ".cnt"
        with open(outputCnt, 'w') as outfile:
            for line in arr_text:
                outfile.write(line+'\n')
        i=0
        arr_vid=[]
        while(i<len(arr_image)):
            img_source=arr_image[i]
            text_input=arr_text[i]
            if text_input==None or text_input =="":
                print("No text");
            else:
                img_source = draw.content(arr_image[i], text_input,font_file,tmp_path,self.wrap_text_len)
            arr_vid.append(mediah.makevid_no_sound(img_source,tmp_path,time_frame))
            i+=1
        for img in arr_image:
            try:
                os.remove(img)
            except:
                pass
        merged_vid=mediah.mergvid(arr_vid , tmp_path)
        mediah.replace_sound_bg(merged_vid,self.bg_sound_path,tmp_path,self.output)
def run(tl,parent_path,outro_path,start_urls,output,max_text_read,wrap_text_len,bg_sound_path=None,logo_path=None,lang='en',part=0,log_enabled=False):
    process = CrawlerProcess({
        'USER_AGENT': 'Googlebot-News/1.0',
        'LOG_ENABLED':log_enabled
    })
    #process.crawl(MSNSpider,bg_sound_path="D:/Developer/Python/reup/msn/bg/01.wav",parent_path="D:/Developer/Python/reup/msn", start_urls=["https://www.msn.com/vi-vn/entertainment/news/v%C3%AC-sao-ng%E1%BB%8Dc-trinh-kh%C3%B4ng-%C4%91%C3%B3ng-phim-v%E1%BA%ABn-c%C3%B3-m%E1%BA%B7t-g%C3%A2y-b%C3%A3o-th%E1%BA%A3m-%C4%91%E1%BB%8F-lhp-cannes/ar-AABD8AV"])
    process.crawl(MSNSpiderAudioBG,outro_path=outro_path,parent_path=parent_path,start_urls=start_urls,output=output,tl=tl,max_text_read=max_text_read,wrap_text_len=wrap_text_len,bg_sound_path=bg_sound_path,logo_path=logo_path,lang=lang,part=part)
    process.start()