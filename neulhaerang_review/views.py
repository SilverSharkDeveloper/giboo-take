from django.db.models import Count
from django.shortcuts import render
from django.views import View
from rest_framework.response import Response
from rest_framework.views import APIView

from neulhaerang_review.models import NeulhaerangReview
from workspace.pagenation import Pagenation
from workspace.serializers import NeulhaerangSerializer, PagenatorSerializer, NeulhaerangReviewSerializer


class NeulhaerangReviewDetailView(View):
    def get(self, request, neulhaerang_review_id):
        post = NeulhaerangReview.objects.get(id=neulhaerang_review_id)
        context = {
            'post':post,
        }
        return render(request,'neulhaerang/review-detail.html',context)


class NeulhaerangReviewListView(View):
    def get(self,request):
        def get(self, request):
            if request.GET.get("page") is not None:
                page = request.GET.get("page")
            else:
                page = 1

        return render(request,'neulhaerang/review-list.html')

class NeulhaerangReviewListAPIView(APIView):
    def get(self, request):
        page = int(request.GET.get("page"))
        sort = request.GET.get("sort")

        neulhaerang_review = NeulhaerangReview.objects.all()

        if(sort == '추천순'):
            neulhaerang_review = neulhaerang_review.annotate(review_like_count=Count('neulhaerangreviewlike')).order_by('-review_like_count','-created_date')
        elif(sort == '최신순'):
            neulhaerang_review = neulhaerang_review.order_by('-created_date')
        #
        pagenator = Pagenation(page=page, page_count=5, row_count=8, query_set=neulhaerang_review)
        posts = NeulhaerangReviewSerializer(pagenator.paged_models, many=True).data
        serialized_pagenator = PagenatorSerializer(pagenator).data


        datas = {
            "posts": posts,
            "pagenator": serialized_pagenator
        }

        return Response(datas)


# class NeulhaerangReviewDetailView(View):
#     def get(self, request, neulhaerang_review_id):
#
#         post = NeulhaerangReview.objects.get(id=neulhaerang_review_id)
#         post_writer_thumb = NeulhaerangReview.objects.filter(id=neulhaerang_review_id).values('member__profile_image')[0]
#         business_plan = BusinessPlan.objects.filter(neulhaerang_id=neulhaerang_id).order_by('-created_date')
#         tags = NeulhaerangTag.objects.filter(neulhaerang_id=neulhaerang_id).order_by('-created_date')
#         if(NeulhaerangReview.objects.filter(neulhaerang_id=neulhaerang_id)):
#             neulhaerang_review = NeulhaerangReview.objects.filter(neulhaerang_id=neulhaerang_id)[0]
#         else:
#             neulhaerang_review = None
#         inner_title_query = NeulhaerangInnerTitle.objects.filter(neulhaerang_id=neulhaerang_id)
#         content_query = NeulhaerangInnerContent.objects.filter(neulhaerang_id=neulhaerang_id)
#         photo_query = NeulhaerangInnerPhotos.objects.filter(neulhaerang_id=neulhaerang_id).order_by('photo_order')
#
#         contents = list(inner_title_query) + list(content_query) + list(photo_query)
#
#         byeoljji = Byeoljji.objects.filter(neulhaerang_id=neulhaerang_id).order_by('byeoljji_rank')
#
#         sorted_contents = sorted(contents, key=lambda item: item.neulhaerang_content_order)
#
#         target_amount = Neulhaerang.objects.filter(id=neulhaerang_id)
#         amount_sum = NeulhaerangDonation.objects.filter(neulhaerang=neulhaerang_id).aggregate(Sum('donation_amount'))
#         likes_count = NeulhaerangLike.objects.filter(neulhaerang_id=neulhaerang_id).count()
#         participants_count = NeulhaerangParticipants.objects.filter(neulhaerang_id=neulhaerang_id).count()
#         reply = NeulhaerangReply.objects.filter(neulhaerang_id=neulhaerang_id)
#         bottom_posts = Neulhaerang.objects.all().order_by('-created_date')[0:4]
#
#
#         if(amount_sum['donation_amount__sum'] is None):
#             amount_sum = {'donation_amount__sum': 0}
#
#         context = {
#             'neulhaerang_id': neulhaerang_id,
#             'post_writer_thumb':post_writer_thumb,
#             'neulhaerang_review':neulhaerang_review,
#             'bottom_posts': bottom_posts,
#             'reply_count': reply.count(),
#             'participants_count' : participants_count,
#             'likes_count' : likes_count,
#             'byeoljjies': byeoljji,
#             'amount_sum': amount_sum['donation_amount__sum'],
#             'target_amount': serializers.serialize("json",target_amount),
#             'tags': tags,
#             'business_plan': serializers.serialize("json",business_plan),
#             'post': post,
#             'contents': serializers.serialize("json",sorted_contents),
#         }
#         return render(request,'neulhaerang/review-detail.html',context)


# class NeulhaerangDetailReplyAPIView(APIView):
#     def get(self, request):
#         my_email = request.session.get('member_email')
#         replyPage = int(request.GET.get('replyPage'))
#         neulhaerang_id = request.GET.get('neulhaerangId')
#         replys_queryset = NeulhaerangReply.objects.all().filter(neulhaerang_id=neulhaerang_id)
#         pagenator = Pagenation(page=replyPage, page_count=5, row_count=5, query_set=replys_queryset)
#         replys = NeulhaerangReplySerializer(pagenator.paged_models, many=True, context={'request': request}).data
#
#         # 베댓을 가져왔는데 3개이상이다 그럼 오더바이 (좋아요 순 , 생성순)으로 최대 3개 가져와 list
#         # 3개면 전체 댓글 가져온거 list 최신순으로 한다? 이게 말이댐?
#         # 페이지네이터해 list+ list
#         if(replyPage==1):
#             # count = replys_queryset.annotate(reply_count=Count('replylike')).filter(reply_count__gt = 10).count()
#             temps = replys_queryset.annotate(reply_count=Count('replylike')).filter(reply_count__gt = 10).order_by('-reply_count','-created_date').annotate(best_reply=Value(True))
#             if(temps.count()>3):
#                 temps = temps[0:3]
#             temp2 = replys_queryset.annotate(reply_count=Count('replylike')).order_by('-created_date')[0:5-temps.count()]
#             sum_temp = list(temps)+list(temp2)
#             replys = NeulhaerangReplySerializer(sum_temp, many=True, context={'request': request}).data
#             datas = {
#                 'replys':replys,
#                 'replys_count':replys_queryset.count(),
#             }
#             return Response(datas)
#         datas = {
#             'replys':replys,
#             'replys_count':replys_queryset.count(),
#
#         }
#
#         return Response(datas)
#
# class NeulhaerangDetailReplyWriteAPIView(APIView):
#     def get(self, request):
#         my_email = request.session.get('member_email')
#         replyCont = request.GET.get('replyCont')
#         neulhaerang_id = request.GET.get('neulhaerangId')
#         member = Member.objects.get(member_email=my_email)
#
#         NeulhaerangReply.objects.create(member=member, neulhaerang_id=neulhaerang_id, reply_content=replyCont)
#
#         return Response(True)
#
# class NeulhaerangDetailReplyDeleteAPIview(APIView):
#     def get(self, request):
#         reply_id = request.GET.get('reply_id')
#         NeulhaerangReply.objects.get(id=reply_id).delete()
#         return Response(True)
#
# class NeulhaerangDetailReplyLikeAPIView(APIView):
#     def get(self, request):
#         my_email = request.session.get('member_email')
#         neulhaerang_reply_id = request.GET.get('reply_id')
#         member = Member.objects.get(member_email=my_email)
#         neulhaerang_reply = NeulhaerangReply.objects.get(id=neulhaerang_reply_id)
#         reply_like = ReplyLike.objects.filter(neulhaerang_reply=neulhaerang_reply, member=member)
#         if reply_like:
#             reply_like.delete()
#         else:
#             ReplyLike.objects.create(neulhaerang_reply=neulhaerang_reply, member=member)
#         reply_like_count = ReplyLike.objects.filter(neulhaerang_reply=neulhaerang_reply).count()
#
#         return Response(reply_like_count)