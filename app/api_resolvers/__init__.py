from flask import Blueprint as bp

bp = bp('api_resolvers', __name__)

from app.api_resolvers import routes
