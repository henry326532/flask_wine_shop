from flask import Flask, render_template

app = Flask(__name__, static_folder='static')


wines = [
    {
        'name':'千日醇',
        'describtion':'金門酒廠以傲人的釀酒工藝及得天獨厚的天然泉水，釀造出絕佳的酒液，酒液清若泉水，流露著芬芳馥郁的高粱香氣，入口甜而爽口，淨醇柔順帶有細緻口感，味道清香甘甜，餘韻迷人，紮實的結構和韻味在口中漫延，充份展現出最佳白酒獨特風味。',
        'price':'電洽',
        'img':'static/wines/千日醇.jpg'
    },
    {
        'name':'58度金門高粱酒',
        'describtion':'源自1962年問世的特級高粱酒，俗稱為「白金龍」，是深具金門酒廠標誌性風格的最大宗酒款之一。',
        'price':'電洽',
        'img':'static/wines/58度金門高粱酒.png'
    },
    {
        'name':'38度金門高粱酒',
        'describtion':'金門酒廠為迎合市場對中、低酒精度數的需求，推出「38度金門高粱酒」，沒有高酒精度的辛辣感，卻依然保留高粱酒香、純、甘、冽的餘韻，輕鬆易飲，適合年輕、年長族群及女性朋友消費飲用。',
        'price':'電洽',
        'img':'static/wines/38度金門高粱酒.jpg'
    }
]

@app.route('/')
def index():
    return render_template('index.html', wines=wines)

if __name__ == '__main__':
    app.run(debug=True)