import time
from selenium import webdriver
import pandas as pd
import urllib


def get_img_src(driver, link):
    try:
        driver.get(link)
        element = driver.find_element_by_xpath('//*[@id="u_0_k"]/div[2]/div[1]/div[2]/div[3]/div/div/div/a/div/img')
        img_src = element.get_attribute("src")
    except Exception:
        img_src = None
    return img_src


def get_video_src(driver, link):
    try:
        driver.get(link)
        element = driver.find_element_by_xpath('//*[@id="u_0_r"]')
        img_src = element.get_attribute("style").replace('background-image: url("', '').replace('");', '')
    except Exception:
        img_src = None
    return img_src


def download_image(link, filename):
    urllib.urlretrieve(link, filename)


def row_img_link_mapper(row, driver):
    if row['Total video plays'] > 0:
        img_url = get_video_src(driver, row['Link to post'])
    else:
        img_url = get_img_src(driver, row['Link to post'])
        if img_url is None:
            img_url = get_video_src(driver, row['Link to post'])
    return img_url


def row_img_download_mapper(row):
    if row['image_url'] is not None:
        filename = "%06d.jpg" % row.index
        filepath = "./images/" + filename
        download_image(row['image_url'], filepath)
        return filename
    else:
        return None


def main():
    driver = webdriver.Chrome('/Users/sumukhavadhani/chromedriver')
    input_df = pd.read_csv("./FacebookDataset_v1.csv")
    input_df.loc[:, 'image_url'] = input_df.apply(lambda x: row_img_link_mapper(x, driver), axis=1)
    input_df.loc[:, 'image_filename'] = input_df.apply(lambda x: row_img_download_mapper(x), axis=1)
    driver.quit()


if __name__ == "__main__":
    main()