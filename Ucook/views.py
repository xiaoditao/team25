from django.contrib.sites import requests
from django.shortcuts import render, redirect
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from datetime import datetime
from django.utils.safestring import mark_safe
from Ucook.forms import (
    LoginForm,
    RegisterForm,
    EditForm,
    ProfileForm,
    HostPostForm,
    GuestPostForm,
    ReviewForm,
)
from Ucook.models import *
from paypal.standard.forms import PayPalPaymentsForm

from django.utils.dateparse import parse_datetime
from django.http import JsonResponse
from django.views.decorators.csrf import ensure_csrf_cookie
import urllib
import requests

import googlemaps
import geopy.distance
from math import sin, cos, sqrt, atan2, radians
import json

gmaps = googlemaps.Client(key="AIzaSyDS6LdCBfhVfvtMPPAcMQBhMW44IXPxDKY")

def login_action(request):
    context = {}
    if request.method == "GET":
        context["form"] = LoginForm()
        return render(request, "Ucook/login.html", context)
    form = LoginForm(request.POST)
    context["form"] = form
    if not form.is_valid():
        return render(request, "Ucook/login.html", context)
    new_user = authenticate(username=form.cleaned_data["username"],
                            password=form.cleaned_data["password"])
    login(request, new_user)
    return redirect(reverse("welcome"))

def logout_action(request):
    logout(request)
    return redirect(reverse("login"))

def register_action(request):
    context = {}
    if request.method == "GET":
        context["form"] = RegisterForm()
        return render(request, "Ucook/register.html", context)
    form = RegisterForm(request.POST)
    context["form"] = form
    if not form.is_valid():
        return render(request, "Ucook/register.html", context)
    new_user = User.objects.create_user(
        username=form.cleaned_data["username"],
        password=form.cleaned_data["password"],
        email=form.cleaned_data["email"],
    )
    new_user.save()
    # new_user_profile = Profile(user=new_user)
    # new_user_profile.save()
    new_user = authenticate(username=form.cleaned_data["username"],
                            password=form.cleaned_data["password"])
    login(request, new_user)
    return redirect(reverse("home"))

def welcome_action(request):
    context={}
    if request.method == 'GET':
        url_host = "https://protected-plains-77518.herokuapp.com/WebApplication?parameter=getAllHostPost"
        # url_host = "http://localhost:8080/WebApplication/WebApplication?parameter=getAllHostPost"
        r_host = requests.get(url_host)
        content_host = r_host.text
        res_host = eval(content_host.__str__())
        context['length_host'] = len(res_host)
        context['res_host'] = res_host
        context['recent_host'] = res_host[0]

        url_guest = "https://protected-plains-77518.herokuapp.com/WebApplication?parameter=getAllGuestPost"
        # url_guest = "http://localhost:8080/WebApplication/WebApplication?parameter=getAllGuestPost"
        r_guest = requests.get(url_guest)
        content_guest = r_guest.text
        res_guest = eval(content_guest.__str__())
        context['length_guest'] = len(res_guest)
        context['res_guest'] = res_guest

        time = datetime.now()
        year = '{:02d}'.format(time.year)
        month = '{:02d}'.format(time.month)
        day = '{:02d}'.format(time.day)
        if day < "15":
            print("<")
            context['time1'] = year + month + day
            context['time2'] = year + month + "25"
        else:
            print(">")
            if time.month != 12:
                context['time1'] = year + month + day
                month = '{:02d}'.format(time.month + 1)
                context['time2'] = year + month + "10"
        return render(request,"Ucook/index.html",context)

# @login_required
# def profile_action(request):
#     context = {}
#     if request.method == "GET":
#         return render(request, "Ucook/profile.html", context)

def detail_action(request):
    context = {}
    if request.method == "GET":
        return render(request, "Ucook/detail.html", context)

@login_required
def mypost_action(request):
    context = {}
    if request.method == "GET":
        return render(request, "Ucook/mypost.html", context)


def explorehost_action(request):
    context = {}

    if request.method == "GET":
        url = "https://protected-plains-77518.herokuapp.com/WebApplication?parameter=getAllHostPost"
        # url = "http://localhost:8080/WebApplication/WebApplication?parameter=getAllHostPost"
        r = requests.get(url)
        content = r.text
        res = eval(content.__str__())
        context["length"] = len(res)
        context["res"] = res
        print(res)
        return render(request, "Ucook/explore-host.html", context)

    if request.method == "POST":
        try:
            foodType = request.POST["foodType"]
            extraInformation = request.POST["extraInformation"]
            date = "20190409"
            url = (
                "https://protected-plains-77518.herokuapp.com/WebApplication?parameter=newGuestPost&"
                # "http://localhost:8080/WebApplication/WebApplication?parameter=newGuestPost^"
                + foodType
                + "&"
                + extraInformation
                + "&"
                + date
            )
            print("url " + url)
            # print("foodType "+request.POST['foodType'])
            # print("extraInformation "+extraInformation)
            r = requests.get(url)
            # r.json()
            print(r)

            url = "https://protected-plains-77518.herokuapp.com/WebApplication?parameter=getAllHostPost"
            # url = "http://localhost:8080/WebApplication/WebApplication?parameter=getAllHostPost"
            r = requests.get(url)
            content = r.text
            res = eval(content.__str__())
            context["length"] = len(res)
            context["res"] = res
            return render(request, "Ucook/explore-host.html", context)
        except:
            context["error"] = "You didn't fill out all the blanks, please try again"
            return render(request, "Ucook/explore-host.html", context)


def explore_guest_action(request):
    context = {}

    if request.method == "GET":
        url = "https://protected-plains-77518.herokuapp.com/WebApplication?parameter=getAllGuestPost"
        # url = "http://localhost:8080/WebApplication/WebApplication?parameter=getAllGuestPost"
        r = requests.get(url)
        content = r.text
        res = eval(content.__str__())
        context["length"] = len(res)
        context["res"] = res
        return render(request, "Ucook/explore-guest.html", context)

    if request.method == "POST":
        try:
            address1 = request.POST["address1"]
            address2 = request.POST["address2"]
            postCode = request.POST["postcode"]
            city = request.POST["city"]
            state = request.POST["state"]
            foodType = request.POST["foodType"]
            extraInformation = request.POST["extraInformation"]
            preferDate = "20190409"
            number = request.POST["number"]

            coords = gmaps.geocode(address1 + " " + city + " " + state)
            lat = coords[0]
            lng = coords[1]

            url = (
                "https://protected-plains-77518.herokuapp.com/WebApplication?parameter=newHostPost&"
                # "http://localhost:8080/WebApplication/WebApplication?parameter=newHostPost^"
                + address1
                + "&"
                + address2
                + "&"
                + postCode
                + "&"
                + city
                + "&"
                + state
                + "&"
                + foodType
                + "&"
                + extraInformation
                + "&"
                + preferDate
                + "&"
                + number
            )
            print("url " + url)
            print("foodType " + request.POST["foodType"])
            print("extraInformation " + extraInformation)
            r = requests.get(url)
            print(r)

            url = "https://protected-plains-77518.herokuapp.com/WebApplication?parameter=getAllGuestPost"
            # url = "http://localhost:8080/WebApplication/WebApplication?parameter=getAllGuestPost"
            r = requests.get(url)
            content = r.text
            res = eval(content.__str__())
            context["length"] = len(res)
            context["res"] = res
            return render(request, "Ucook/explore-guest.html", context)
        except:
            context["error"] = "You didn't fill out all the blanks, please try again"
            return render(request, "Ucook/explore-guest.html", context)


def comment_action(request):
    context={}
    if request.method == 'GET':
        return render(request, "Ucook/comment.html", context)
    if request.method == "POST":
        print("user", request.user.username)
        try:
            comment = request.POST["contact-message"]
            print("message", comment)
            rate = request.POST["rating"]
            print("rate", rate)
            url = (
                    "https://protected-plains-77518.herokuapp.com/WebApplication?parameter=makeComment&rate="
                    # "http://localhost:8080/WebApplication/WebApplication?parameter=newGuestPost^"
                    + rate
                    + "&comment="
                    + comment
                    + "&Username="
                    + request.user.username
                )
            print("url " + url)
            r = requests.get(url)
            print(r)
            content = r.text
            res = eval(content.__str__())
            context["length"] = len(res)
            context["res"] = res
            return redirect(reverse("profile"))
        except:
            context["error"] = "You didn't fill out all the blanks, please try again"
            return redirect(reverse("profile"))

        # return render(request, "Ucook/profile.html", context)


def welcome_host_action(request):
    context = {}
    if request.method == "GET":
        return render(request, "Ucook/posthost.html", context)


def welcome_guest_action(request):
    context = {}
    if request.method == "GET":
        return render(request, "Ucook/postnonhost.html", context)


def socketio(request):
    return redirect(reverse("welcome"))


def profile_action(request):
    context = {}
    if request.method == "GET":
        paypal_dict = {
            "business": "shituo1209@163.com",
            "amount": "10.00",
            "currency_code": "USD",
            "item_name": "Premium",
            "invoice": "unique invoice-0001",
            "notify_url": request.build_absolute_uri(reverse("paypal-ipn")),
            "return_url": request.build_absolute_uri(reverse("profile")),
            "cancel_return": request.build_absolute_uri(reverse("profile")),
        }
        form = PayPalPaymentsForm(initial=paypal_dict)
        context["form"] = form


        time = datetime.now()
        year = '{:02d}'.format(time.year)
        month = '{:02d}'.format(time.month)
        day = '{:02d}'.format(time.day)
        context['time'] = year+month+day

        # Get comment and rating
        url_comment = "https://protected-plains-77518.herokuapp.com/WebApplication?parameter=getComment&username=kaidiz"
        # url_comment = "http://localhost:8080/WebApplication/WebApplication?parameter=getComment%5Ekaidiz"
        r_comment = requests.get(url_comment)
        content_comment = r_comment.text
        res_comment = eval(content_comment.__str__())
        context['length_comment'] = len(res_comment)
        context['res_comment'] = res_comment
        rating_sum = 0
        for i in range(len(res_comment)):
            rating_sum += res_comment[i].get('rate')
        context['rating'] = '{:.2f}'.format(rating_sum / len(res_comment))

        # Post when I am the guest
        url_history = "https://protected-plains-77518.herokuapp.com/WebApplication?parameter=getHistory&username=kaidiz"
        # url_user = "http://localhost:8080/WebApplication/WebApplication?parameter=getHistory%5Ekaidiz"
        r_history = requests.get(url_history)
        content_history = r_history.text
        hrefDict = {}
        if content_history.__str__().__len__() != 0:
            res_history = eval(content_history.__str__())
            context['length_history'] = len(res_history)
            context['res_history'] = res_history
            print(res_history[0]['postID'])
            print(request.user.username)
            for i in range(len(res_history)):
                ID = res_history[i]['postID']
                username = request.user.username
                MyUrl = "https://stark-forest-73611.herokuapp.com/ChattingHistory?type=encrypt&content="+str(ID)+"-"+username
                encrypt = requests.get(MyUrl)
                encrypt_comment = encrypt.text
                print(encrypt_comment)
                encrypt_comment = 'http://13.58.161.243:8000/chat/'+encrypt_comment
                hrefDict[ID] = encrypt_comment
                print(hrefDict)
        context['hrefDict'] = mark_safe(json.dumps(hrefDict))


        # Post when I am the host
        url_post= "https://protected-plains-77518.herokuapp.com/WebApplication?parameter=getPost&Username=kaidiz"
        r_post = requests.get(url_post)
        content_post = r_post.text
        if content_post.__str__().__len__() != 0:
            res_post = eval(content_post.__str__())
            context['length_post'] = len(res_post)
            context['res_post'] = res_post
            print(res_post)

        # Chatting
        username = request.user.username

        return render(request, "Ucook/profile.html", context)



@login_required
def post_host_action(request):
    assert request.method == "POST"
    context = {}
    form = HostPostForm(request.POST or None)
    if not form.is_valid():
        return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
    # call cloud db API
    context["content"] = form.cleaned_data
    return render(request, "post-host-detail", context)


@login_required
def post_guest_action(request):
    assert request.method == "POST"
    context = {}
    form = GuestPostForm(request.POST or None)
    if not form.is_valid():
        return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
    # call cloud db API
    context["content"] = form.cleaned_data["content"]
    context["cuisine_type"] = form.cleaned_data["cuisine_type"]
    context["preferred_date"] = form.cleaned_data["preferred_date"]
    return render(request, "post-guest-detail", context)


def closest_posts_action(request):
    # take out request param for the current center
    center_lat = request.GET.get("lat")
    center_lng = request.GET.get("lng")

    # call cloud db API for all host/guest posts
    posts = [
        {
            "owner": "dummy",
            "address1": "3913 Nantasket Street",
            "address2": "11",
            "postCode": "15207",
            "city": "Pittsburgh",
            "state": "Pennsylvania",
            "coordinates": {"lat": 40.4273999, "lng": -79.9403981},
        },
        {
            "owner": "dummy1",
            "address1": "5030 Centre Avenue",
            "address2": "961",
            "postCode": "15213",
            "city": "Pittsburgh",
            "state": "Pennsylvania",
            "coordinates": {"lat": 40.4537737, "lng": -79.9431412},
        },
        {
            "owner": "dummy2",
            "address1": "4716 Ellsworth Avenue",
            "address2": "11",
            "postCode": "15213",
            "city": "Pittsburgh",
            "state": "Pennsylvania",
            "coordinates": {"lat": 40.4483713, "lng": -79.946681},
        },
        {
            "owner": "dummy3",
            "address1": "2 Bayard Road",
            "address2": "23",
            "postCode": "15213",
            "city": "Pittsburgh",
            "state": "Pennsylvania",
            "coordinates": {"lat": 40.4534333, "lng": -79.9427924},
        },
        {
            "owner": "dummy4",
            "address1": "5000 Forbes Avenue",
            "address2": "11",
            "postCode": "15213",
            "city": "Pittsburgh",
            "state": "Pennsylvania",
            "coordinates": {"lat": 40.44416469999999, "lng": -79.9433725},
        },
        {
            "owner": "dummy6",
            "address1": "239 ATWOOD ST",
            "postCode": "15213",
            "city": "Pittsburgh",
            "state": "Pennsylvania",
            "coordinates": {"lat": 40.44036937, "lng": -79.95628244},
        },
        {
            "owner": "dummy7",
            "address1": "3609 FORBES AV",
            "postCode": "15213",
            "city": "Pittsburgh",
            "state": "Pennsylvania",
            "coordinates": {"lat": 40.44076978, "lng": -79.95815268},
        },
        {
            "owner": "dummy8",
            "address1": "3800 FIFTH AV",
            "postCode": "15213",
            "city": "Pittsburgh",
            "state": "Pennsylvania",
            "coordinates": {"lat": 40.44234167, "lng": -79.9574109},
        },
        {
            "owner": "dummy9",
            "address1": "214 OAKLAND AV",
            "postCode": "15213",
            "city": "Pittsburgh",
            "state": "Pennsylvania",
            "coordinates": {"lat": 40.44082789, "lng": -79.95568695},
        },
        {
            "owner": "dummy10",
            "address1": "3907 FORBES AV",
            "postCode": "15213",
            "city": "Pittsburgh",
            "state": "Pennsylvania",
            "coordinates": {"lat": 40.44223638, "lng": -79.95616413},
        },
        {
            "owner": "dummy11",
            "address1": "100 ATWOOD ST",
            "postCode": "15213",
            "city": "Pittsburgh",
            "state": "Pennsylvania",
            "coordinates": {"lat": 40.44182082, "lng": -79.95831233},
        },
        {
            "owner": "dummy12",
            "address1": "3700 FORBES AV",
            "postCode": "15213",
            "city": "Pittsburgh",
            "state": "Pennsylvania",
            "coordinates": {"lat": 40.44123704, "lng": -79.95740996},
        },
        {
            "owner": "dummy13",
            "address1": "3700 FORBES AV",
            "postCode": "15213",
            "city": "Pittsburgh",
            "state": "Pennsylvania",
            "coordinates": {"lat": 40.44123704, "lng": -79.95740996},
        },
        {
            "owner": "dummy14",
            "address1": "100 ATWOOD ST",
            "postCode": "15213",
            "city": "Pittsburgh",
            "state": "Pennsylvania",
            "coordinates": {"lat": 40.44182082, "lng": -79.95831233},
        },
        {
            "owner": "dummy15",
            "address1": "3900 FORBES AV",
            "postCode": "15213",
            "city": "Pittsburgh",
            "state": "Pennsylvania",
            "coordinates": {"lat": 40.44208775, "lng": -79.9561512},
        },
        {
            "owner": "dummy16",
            "address1": "3900 FORBES AV",
            "postCode": "15213",
            "city": "Pittsburgh",
            "state": "Pennsylvania",
            "coordinates": {"lat": 40.44208775, "lng": -79.9561512},
        },
        {
            "owner": "dummy17",
            "address1": "200 ATWOOD ST",
            "postCode": "15213",
            "city": "Pittsburgh",
            "state": "Pennsylvania",
            "coordinates": {"lat": 40.44122178, "lng": -79.9575148},
        },
        {
            "owner": "dummy18",
            "address1": "100 OAKLAND AV",
            "postCode": "15213",
            "city": "Pittsburgh",
            "state": "Pennsylvania",
            "coordinates": {"lat": 40.44231467, "lng": -79.9575101},
        },
        {
            "owner": "dummy19",
            "address1": "223 ATWOOD ST",
            "postCode": "15213",
            "city": "Pittsburgh",
            "state": "Pennsylvania",
            "coordinates": {"lat": 40.44102886, "lng": -79.95708769},
        },
        {
            "owner": "dummy20",
            "address1": "3600 FORBES AV",
            "postCode": "15213",
            "city": "Pittsburgh",
            "state": "Pennsylvania",
            "coordinates": {"lat": 40.44065047, "lng": -79.95809936},
        },
        {
            "owner": "dummy21",
            "address1": "100 N BOUQUET ST",
            "postCode": "15213",
            "city": "Pittsburgh",
            "state": "Pennsylvania",
            "coordinates": {"lat": 40.44250806, "lng": -79.95728335},
        },
        {
            "owner": "dummy22",
            "address1": "100 MEYRAN AV",
            "postCode": "15213",
            "city": "Pittsburgh",
            "state": "Pennsylvania",
            "coordinates": {"lat": 40.44132082, "lng": -79.95901234},
        },
        {
            "owner": "dummy23",
            "address1": "214 OAKLAND AV",
            "postCode": "15213",
            "city": "Pittsburgh",
            "state": "Pennsylvania",
            "coordinates": {"lat": 40.44082789, "lng": -79.95568695},
        },
        {
            "owner": "dummy24",
            "address1": "3900 FORBES AV",
            "postCode": "15213",
            "city": "Pittsburgh",
            "state": "Pennsylvania",
            "coordinates": {"lat": 40.44208775, "lng": -79.9561512},
        },
        {
            "owner": "dummy25",
            "address1": "3800 FORBES AV",
            "postCode": "15213",
            "city": "Pittsburgh",
            "state": "Pennsylvania",
            "coordinates": {"lat": 40.44164308, "lng": -79.95670703},
        },
        {
            "owner": "dummy26",
            "address1": "200 S BOUQUET ST",
            "postCode": "15213",
            "city": "Pittsburgh",
            "state": "Pennsylvania",
            "coordinates": {"lat": 40.4414964, "lng": -79.95526271},
        },
        {
            "owner": "dummy27",
            "address1": "252 OAKLAND AV",
            "postCode": "15213",
            "city": "Pittsburgh",
            "state": "Pennsylvania",
            "coordinates": {"lat": 40.44041241, "lng": -79.95519815},
        },
        {
            "owner": "dummy28",
            "address1": "223 ATWOOD ST",
            "postCode": "15213",
            "city": "Pittsburgh",
            "state": "Pennsylvania",
            "coordinates": {"lat": 40.44102886, "lng": -79.95708769},
        },
        {
            "owner": "dummy29",
            "address1": "3600 FORBES AV",
            "postCode": "15213",
            "city": "Pittsburgh",
            "state": "Pennsylvania",
            "coordinates": {"lat": 40.44065047, "lng": -79.95809936},
        },
        {
            "owner": "dummy30",
            "address1": "3900 FORBES AV",
            "postCode": "15213",
            "city": "Pittsburgh",
            "state": "Pennsylvania",
            "coordinates": {"lat": 40.44208775, "lng": -79.9561512},
        },
        {
            "owner": "dummy31",
            "address1": "100 DESOTO ST",
            "postCode": "15213",
            "city": "Pittsburgh",
            "state": "Pennsylvania",
            "coordinates": {"lat": 40.44231637, "lng": -79.95773576},
        },
        {
            "owner": "dummy32",
            "address1": "3700 FORBES AV",
            "postCode": "15213",
            "city": "Pittsburgh",
            "state": "Pennsylvania",
            "coordinates": {"lat": 40.44123704, "lng": -79.95740996},
        },
        {
            "owner": "dummy33",
            "address1": "3900 FORBES AV",
            "postCode": "15213",
            "city": "Pittsburgh",
            "state": "Pennsylvania",
            "coordinates": {"lat": 40.44208775, "lng": -79.9561512},
        },
        {
            "owner": "dummy34",
            "address1": "248 OAKLAND AV",
            "postCode": "15213",
            "city": "Pittsburgh",
            "state": "Pennsylvania",
            "coordinates": {"lat": 40.44045556, "lng": -79.95524891},
        },
        {
            "owner": "dummy35",
            "address1": "3609 FORBES AV",
            "postCode": "15213",
            "city": "Pittsburgh",
            "state": "Pennsylvania",
            "coordinates": {"lat": 40.44076978, "lng": -79.95815268},
        },
        {
            "owner": "dummy36",
            "address1": "3705 FIFTH AV",
            "postCode": "15213",
            "city": "Pittsburgh",
            "state": "Pennsylvania",
            "coordinates": {"lat": 40.44220233, "lng": -79.9579311},
        },
        {
            "owner": "dummy37",
            "address1": "100 OAKLAND AV",
            "postCode": "15213",
            "city": "Pittsburgh",
            "state": "Pennsylvania",
            "coordinates": {"lat": 40.44231467, "lng": -79.9575101},
        },
        {
            "owner": "dummy38",
            "address1": "3609 FORBES AV",
            "postCode": "15213",
            "city": "Pittsburgh",
            "state": "Pennsylvania",
            "coordinates": {"lat": 40.44076978, "lng": -79.95815268},
        },
        {
            "owner": "dummy39",
            "address1": "3609 FORBES AV",
            "postCode": "15213",
            "city": "Pittsburgh",
            "state": "Pennsylvania",
            "coordinates": {"lat": 40.44076978, "lng": -79.95815268},
        },
        {
            "owner": "dummy40",
            "address1": "3909 FORBES AV",
            "postCode": "15213",
            "city": "Pittsburgh",
            "state": "Pennsylvania",
            "coordinates": {"lat": 40.44225947, "lng": -79.95613528},
        },
        {
            "owner": "dummy41",
            "address1": "210 OAKLAND AV",
            "postCode": "15213",
            "city": "Pittsburgh",
            "state": "Pennsylvania",
            "coordinates": {"lat": 40.44087264, "lng": -79.9557396},
        },
        {
            "owner": "dummy42",
            "address1": "3800 SENNOTT ST",
            "postCode": "15213",
            "city": "Pittsburgh",
            "state": "Pennsylvania",
            "coordinates": {"lat": 40.4410469, "lng": -79.95580304},
        },
        {
            "owner": "dummy43",
            "address1": "3700 FORBES AV",
            "postCode": "15213",
            "city": "Pittsburgh",
            "state": "Pennsylvania",
            "coordinates": {"lat": 40.44123704, "lng": -79.95740996},
        },
        {
            "owner": "dummy44",
            "address1": "3900 FORBES AV",
            "postCode": "15213",
            "city": "Pittsburgh",
            "state": "Pennsylvania",
            "coordinates": {"lat": 40.44208775, "lng": -79.9561512},
        },
        {
            "owner": "dummy45",
            "address1": "107 THACKERY AV",
            "postCode": "15213",
            "city": "Pittsburgh",
            "state": "Pennsylvania",
            "coordinates": {"lat": 40.44334624, "lng": -79.95655891},
        },
        {
            "owner": "dummy46",
            "address1": "3705 FIFTH AV",
            "postCode": "15213",
            "city": "Pittsburgh",
            "state": "Pennsylvania",
            "coordinates": {"lat": 40.44220233, "lng": -79.9579311},
        },
        {
            "owner": "dummy47",
            "address1": "3705 FIFTH AV",
            "postCode": "15213",
            "city": "Pittsburgh",
            "state": "Pennsylvania",
            "coordinates": {"lat": 40.44220233, "lng": -79.9579311},
        },
        {
            "owner": "dummy48",
            "address1": "3901 FORBES AV",
            "postCode": "15213",
            "city": "Pittsburgh",
            "state": "Pennsylvania",
            "coordinates": {"lat": 40.44216359, "lng": -79.95625513},
        },
        {
            "owner": "dummy49",
            "address1": "221 ATWOOD ST",
            "postCode": "15213",
            "city": "Pittsburgh",
            "state": "Pennsylvania",
            "coordinates": {"lat": 40.44105318, "lng": -79.95711693},
        },
        {
            "owner": "dummy50",
            "address1": "3801 FORBES AV",
            "postCode": "15213",
            "city": "Pittsburgh",
            "state": "Pennsylvania",
            "coordinates": {"lat": 40.44171892, "lng": -79.95681096},
        },
        {
            "owner": "dummy51",
            "address1": "3609 FORBES AV",
            "postCode": "15213",
            "city": "Pittsburgh",
            "state": "Pennsylvania",
            "coordinates": {"lat": 40.44076978, "lng": -79.95815268},
        },
        {
            "owner": "dummy52",
            "address1": "3700 FORBES AV",
            "postCode": "15213",
            "city": "Pittsburgh",
            "state": "Pennsylvania",
            "coordinates": {"lat": 40.44123704, "lng": -79.95740996},
        },
        {
            "owner": "dummy53",
            "address1": "3907 FORBES AV",
            "postCode": "15213",
            "city": "Pittsburgh",
            "state": "Pennsylvania",
            "coordinates": {"lat": 40.44223638, "lng": -79.95616413},
        },
        {
            "owner": "dummy54",
            "address1": "3803 FORBES AV",
            "postCode": "15213",
            "city": "Pittsburgh",
            "state": "Pennsylvania",
            "coordinates": {"lat": 40.44172644, "lng": -79.95680156},
        },
        {
            "owner": "dummy55",
            "address1": "3600 FORBES AV",
            "postCode": "15213",
            "city": "Pittsburgh",
            "state": "Pennsylvania",
            "coordinates": {"lat": 40.44065047, "lng": -79.95809936},
        },
        {
            "owner": "dummy56",
            "address1": "3900 FORBES AV",
            "postCode": "15213",
            "city": "Pittsburgh",
            "state": "Pennsylvania",
            "coordinates": {"lat": 40.44208775, "lng": -79.9561512},
        },
        {
            "owner": "dummy57",
            "address1": "3900 FIFTH AV",
            "postCode": "15213",
            "city": "Pittsburgh",
            "state": "Pennsylvania",
            "coordinates": {"lat": 40.44255153, "lng": -79.95719574},
        },
        {
            "owner": "dummy58",
            "address1": "3705 FIFTH AV",
            "postCode": "15213",
            "city": "Pittsburgh",
            "state": "Pennsylvania",
            "coordinates": {"lat": 40.44220233, "lng": -79.9579311},
        },
        {
            "owner": "dummy59",
            "address1": "200 ATWOOD ST",
            "postCode": "15213",
            "city": "Pittsburgh",
            "state": "Pennsylvania",
            "coordinates": {"lat": 40.44122178, "lng": -79.9575148},
        },
        {
            "owner": "dummy60",
            "address1": "3800 FORBES AV",
            "postCode": "15213",
            "city": "Pittsburgh",
            "state": "Pennsylvania",
            "coordinates": {"lat": 40.44164308, "lng": -79.95670703},
        },
        {
            "owner": "dummy61",
            "address1": "214 OAKLAND AV",
            "postCode": "15213",
            "city": "Pittsburgh",
            "state": "Pennsylvania",
            "coordinates": {"lat": 40.44082789, "lng": -79.95568695},
        },
        {
            "owner": "dummy62",
            "address1": "200 OAKLAND AV",
            "postCode": "15213",
            "city": "Pittsburgh",
            "state": "Pennsylvania",
            "coordinates": {"lat": 40.4409813, "lng": -79.95586744},
        },
        {
            "owner": "dummy63",
            "address1": "3900 FORBES AV",
            "postCode": "15213",
            "city": "Pittsburgh",
            "state": "Pennsylvania",
            "coordinates": {"lat": 40.44208775, "lng": -79.9561512},
        },
    ]
    # for post in posts:
    #     coords = gmaps.geocode(
    #         post["address1"] + " " + post["city"] + " " + post["state"]
    #     )
    #     print(coords)

    # compute distances between all posts and the current center
    # max_dist = 1  # max dist in km
    max_dist = 0.5
    posts = list(
        filter(
            lambda obj: cal_dist_in_km(
                obj["coordinates"]["lat"],
                obj["coordinates"]["lng"],
                center_lat,
                center_lng,
            )
            <= max_dist,
            posts,
        )
    )

    # return the closest posts as json objects to the user
    json_posts = json.dumps({"posts": posts}, indent=4)
    return HttpResponse(json_posts, content_type="application/json")


def cal_dist_in_km(lat1, lng1, lat2, lng2):

    if not isinstance(lat1, float):
        lat1 = float(lat1)
    if not isinstance(lng1, float):
        lng1 = float(lng1)
    if not isinstance(lat2, float):
        lat2 = float(lat2)
    if not isinstance(lng2, float):
        lng2 = float(lng2)

    dist = geopy.distance.vincenty((lat1, lng1), (lat2, lng2)).km

    # print(dist)

    return dist
