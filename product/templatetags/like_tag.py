from django import template
from product.models import Product,Like

register = template.Library()


# @register.simple_tag(takes_context=True)
# def is_liked(context,post_id):
#     request = context ['request']
#     if request.user.id is None:
#         user_inst=User.objects.get(username=str(request.session.session_key))
#         try:
#             likes= BlogLikes.objects.get(post__id=post_id,liked_by=user_inst).like
#         except Exception as e:
#             likes=False
#         return likes
#     else:
#         try:
#             likes= BlogLikes.objects.get(post__id=post_id,liked_by=request.user.id).like
#         except Exception as e:
#             likes=False
#         return likes



@register.simple_tag()
def count_likes(post_id):
    return Like.objects.filter(product_id=post_id).count()


# @register.simple_tag(takes_context=True)
# def likes_id(context,post_id):
#     request = context['request']
#     if request.user.id is None:
#         user_inst=User.objects.get(username=str(request.session.session_key))
#         return BlogLikes.objects.get(post__id=post_id,liked_by=user_inst.id).id
#     else:
#         return BlogLikes.objects.get(post__id=post_id,liked_by=request.user).id
    