import scrapy

class AnimeLink(scrapy.Spider):
    name = "anime"

    def start_requests(self):
        url = "http://voiranime.to/?post_type=wp-manga&s="
        search = getattr(self, "search", None)
        if search is not None:
            url = "{}{}".format(url, search)
            yield scrapy.Request(url, self.parse)
        else:
            raise Exception("You must specify a search")

    def parse(self, response):
        yield from response.follow_all(css="div.post-title a", callback=self.anime_item_search)

    def get_episode_page(self, response):
        url = response.css("div.reading-content iframe::attr(src)").get()
        title = response.css("ol.breadcrumb li.active::text").get()
        yield response.follow(url, self.get_download_url, cb_kwargs=dict(title=title))

    def get_download_url(self, response, title):
        for script in response.css("script::text").getall():
            if len(script.split('eval(function')) > 1:
                ext = script.split("ready|")[1].split('|')[1].strip()
                type_and_video = script.split("type|")[1].split('|')
                video_token = type_and_video[0]
                sub_domain = type_and_video[1].split('\'')[0]
                download_link = "https://{}.gounlimited.to/{}/v.{}".format(sub_domain, video_token, ext)
                #self.anime.update({"download_link": download_link})
                yield {
                    "title": title,
                    "download_link": download_link
                }

    def anime_item_search(self, response):
        anime = {}
        for post_content in response.css("div.post-content_item"):
            index = post_content.css("div.summary-heading h5::text").get().strip()
            value = post_content.css("div.summary-content::text").get().strip()
            if post_content.css("span#averagerate").get() is not None:
                anime.update({index: post_content.css("span#averagerate::text").get()})
            else:
                anime.update({index: value})

        #chapters = response.css("li.wp-manga-chapter")
        #chaps = []
        #self.anime = anime
        #yield {"anime": anime}
        yield from response.follow_all(css="li.wp-manga-chapter a", callback=self.get_episode_page)