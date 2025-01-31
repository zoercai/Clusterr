import json
from flask import Flask, render_template, request, Response
from ArticlesRetriever import retrieve_articles
from Cluster.Clusterer import cluster
from WebAppProcessor import process

app = Flask(__name__)


@app.route('/')
def index():
    # Renders the initial page for user input
    return render_template('index.html')


@app.route('/cluster')
def clusterer():
    # Called when user clicks submit, clusters, and returns result in JSON

    results = request.args.get('results')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    cluster_num = request.args.get('clusters', 5, type=int)

    # retrieve articles
    articles_list = retrieve_articles(results, start_date, end_date)

    # cluster articles
    final_matrix, tfidf_vectorizer, clusters, cluster_centers = cluster(articles_list, cluster_num)

    # process clusters
    node_list, link_list = process(final_matrix, tfidf_vectorizer, articles_list, clusters, cluster_centers)

    # format & jsonify
    json_nodelist = json.dumps([ob.__dict__ for ob in node_list])
    json_linklist = json.dumps([ob.__dict__ for ob in link_list])
    final = '{"nodes":' + json_nodelist + ', "links":' + json_linklist + '}'

    # print(final)

    resp = Response(response=final,
                    status=200,
                    mimetype="application/json")

    return resp


if __name__ == '__main__':
    app.run()
