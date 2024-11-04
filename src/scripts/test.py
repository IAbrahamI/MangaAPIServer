import manganelo

home_page = manganelo.get_home_page()
results = manganelo.get_search_results("Path of the Shaman")


for title in results:
    print(title.title, title.views)

    chapters = title.chapter_list
    
    #icon_path = title.download_icon("./icon.png")
    print(title.icon_url)
    #chapter_path = chapters[-1].download(f"./Chapter {chapters[-1].chapter}.pdf")
    #print(f"./Chapter {chapters[-1].chapter}.pdf")

    """for c in chapters:
        print(f"#{c.chapter} | {c.title}")
        print(print(c.download(f"./Chapter {c.chapter}.pdf")))"""
        #chapter_path = c.download(f"./Chapter {c.chapter}.pdf")