
import os
import json
import networkx as nx
import requests
from flask import Flask, request, jsonify, send_from_directory

# 配置
LASTFM_API_KEY = os.getenv('LASTFM_API_KEY', '3bb23251ac9d599659ba4e31a9a9ea56')  # 请替换为你的key或用环境变量
DATA_DIR = os.path.dirname(os.path.abspath(__file__))

# 载入本地数据
with open(os.path.join(DATA_DIR, 'all_lyrics_analysis_merged.json'), encoding='utf-8') as f:
    lyrics_data = json.load(f)
with open(os.path.join(DATA_DIR, 'top_100_western_artists.json'), encoding='utf-8') as f:
    artist_meta = {item['name']: item for item in json.load(f)}

# 载入知识图谱
G = nx.read_graphml(os.path.join(DATA_DIR, 'artist_network_all_features.graphml'))

app = Flask(__name__)

def get_lastfm_artist_info(artist_name):
    url = f'https://ws.audioscrobbler.com/2.0/?method=artist.getinfo&artist={artist_name}&api_key={LASTFM_API_KEY}&format=json'
    resp = requests.get(url)
    if resp.status_code == 200:
        return resp.json().get('artist', {})
    return {}

def get_lastfm_similar_artists(artist_name):
    url = f'https://ws.audioscrobbler.com/2.0/?method=artist.getsimilar&artist={artist_name}&api_key={LASTFM_API_KEY}&format=json&limit=5'
    resp = requests.get(url)
    if resp.status_code == 200:
        return resp.json().get('similarartists', {}).get('artist', [])
    return []

def get_local_recommendations(artist_name, topn=5):
    if artist_name not in G:
        return []
    neighbors = G[artist_name]
    ranked = sorted(neighbors.items(), key=lambda x: float(x[1].get('weight', 0)), reverse=True)
    return [n for n, _ in ranked[:topn]]


# API: 获取艺人信息（支持模糊匹配）
from difflib import get_close_matches

@app.route('/api/artist')
def api_artist():
    artist_query = request.args.get('name', '').strip()
    result = {}
    all_artists = list(artist_meta.keys())
    # 如果没有查询参数，返回所有艺人名（用于前端自动补全）
    if not artist_query:
        return jsonify({'all_artists': all_artists})

    # 先尝试精确匹配
    matched_artist = artist_meta.get(artist_query)
    best_match = artist_query
    # 如果没有精确匹配，使用difflib模糊匹配
    if not matched_artist:
        matches = get_close_matches(artist_query, all_artists, n=1, cutoff=0.6)
        if matches:
            best_match = matches[0]
            matched_artist = artist_meta.get(best_match)
    # 如果还没有匹配，尝试包含关系
    if not matched_artist:
        contains = [a for a in all_artists if artist_query.lower() in a.lower()]
        if contains:
            best_match = contains[0]
            matched_artist = artist_meta.get(best_match)

    if matched_artist:
        meta = matched_artist
        songs = lyrics_data.get(best_match, {})
        lastfm_info = get_lastfm_artist_info(best_match)
        lastfm_similar = get_lastfm_similar_artists(best_match)
        local_recs = get_local_recommendations(best_match)
        result = {
            'meta': meta,
            'songs': songs,
            'lastfm_info': lastfm_info,
            'lastfm_similar': lastfm_similar,
            'local_recs': local_recs,
            'matched_name': best_match
        }
    return jsonify(result)

# 静态文件服务
@app.route('/')
def index():
    return send_from_directory('static', 'index.html')

@app.route('/<path:path>')
def static_proxy(path):
    return send_from_directory('static', path)

if __name__ == '__main__':
    app.run(debug=True)
