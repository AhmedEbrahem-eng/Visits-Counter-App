from flask import Blueprint, render_template, jsonify, current_app
import logging
import redis
import os

main_bp = Blueprint("main", __name__)
logger = logging.getLogger(__name__)

def get_hit_count():
    from app import cache
    retries = 5
    while True:
        try:
            return cache.incr("hits")
        except redis.exceptions.ConnectionError as exc:
            if retries == 0:
                logger.error("Failed to connect to Redis after 5 retries.")
                raise exc
            retries -= 1

@main_bp.route("/")
def index():
    try:
        count = get_hit_count()
        error = None
    except Exception as e:
        logger.error(f"Error fetching hit count: {e}")
        count = 0
        error = "Redis database connection offline."
        
    return render_template("index.html", count=count, error=error)

@main_bp.route("/api/count", methods=["GET"])
def get_count_api():
    from app import cache
    try:
        count = cache.get("hits") or 0
        return jsonify({"status": "success", "count": int(count)})
    except Exception as e:
        logger.error(f"API Error fetching hit count: {e}")
        return jsonify({"status": "error", "message": "Redis offline"}), 500

@main_bp.route("/api/increment", methods=["POST"])
def increment_count_api():
    try:
        count = get_hit_count()
        return jsonify({"status": "success", "count": count})
    except Exception as e:
        logger.error(f"API Error incrementing count: {e}")
        return jsonify({"status": "error", "message": "Redis offline"}), 500

@main_bp.route("/health")
def health():
    from app import cache
    try:
        cache.ping()
        return jsonify({
            "status": "healthy",
            "redis": "connected"
        }), 200
    except Exception as e:
        logger.critical(f"Health check failed: {e}")
        return jsonify({
            "status": "unhealthy",
            "redis": "disconnected",
            "error": str(e)
        }), 503
