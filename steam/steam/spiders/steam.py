import scrapy


class SteamSpider(scrapy.Spider):
    name = 'steam'
    # allowed_domains = ['store.steampowered.com']
    start_urls = [f'https://store.steampowered.com/search/?filter=topsellers&page={i}' for i in range(1,20)]
    # start_urls = ['https://store.steampowered.com/search/?filter=topsellers&page=1']

    def parse(self, response):
        for link in response.xpath('//a[@data-gpnav="item"]'):
            game_page = link.xpath('./@href').get()

            yield scrapy.Request(game_page, callback=self.parse_game)
    
            # yield{
            #     'game_page' : game_page,
            # }

        # next_page = response.xpath('//a[@class="pagebtn"]/@href').get()
        # if next_page:
        #     yield scrapy.Request(url=next_page, callback=self.parse)

    
    def parse_game(self, response):
        for j in response.xpath('//div[@class="page_content_ctn"]'):
            title = j.xpath('.//div[@class="apphub_AppName"]//text()').get()
            feedback = j.xpath('.//span[@class="nonresponsive_hidden responsive_reviewdesc"]//text()').getall()
            description = j.xpath('.//div[@class="game_description_snippet"]//text()').getall()
            filters = j.xpath('.//div[@class="glance_tags popular_tags"]//text()').getall()
            resources = j.xpath('.//a[@class="game_area_details_specs_ctn"]//text()').getall()
            details = j.xpath('.//div[@class="details_block"]//text()').getall()
            final_price = j.xpath('.//div[@class="discount_original_price"]//text()').get()
            original_price = j.xpath('.//div[@class="discount_final_price"]//text()').get()

            yield{
                'title' : title,
                'feedback' : feedback,
                'description' : description,
                'filters' : filters,
                'resources' : resources,
                'details' : details,
                'final_price' : final_price,
                'original_price' : original_price
            }


    # with open('artigos_aj.csv', 'a', newline='', encoding="utf-8")  as output_file:
    #     dict_writer = csv.DictWriter(output_file, post.keys())            
    #     dict_writer.writerows([post])        
    # yield post