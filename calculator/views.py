from django.shortcuts import redirect, render
from django.http import JsonResponse
from django.urls import reverse
from django.utils import timezone

from urllib.parse import urlencode

from .forms import *


def index(request):
    data = None
    investmentWorth = None
    # When redirects to url with get parameters read url and get the parameters, put them into the form
    if request.method == "GET":
        form = InvestmentsForm()

        try:
            startingAmount = int(request.GET["starting-amount"])
            additionalContribution = int(
                request.GET["additional-contribution"])
            additionalContributionFrequency = int(
                request.GET["additional-contribution-frequency"])
            rateOfReturn = int(request.GET["rate-of-return"])
            yearsToGrow = int(request.GET["years-to-grow"])

            investmentData = getDataFromParameters(
                startingAmount, additionalContribution, additionalContributionFrequency, rateOfReturn, yearsToGrow)
            data = investmentData[0]
            investmentWorth = investmentData[1]

            form = InvestmentsForm({
                "startingAmount": startingAmount,
                "additionalContribution": additionalContribution,
                "additionalContributionFrequency": additionalContributionFrequency,
                "rateOfReturn": rateOfReturn,
                "yearsToGrow": yearsToGrow
            })

        except:
            form = InvestmentsForm()

        # On post method check form
    if request.method == "POST":
        form = InvestmentsForm(request.POST)

        # If valid make username lowercase, authenticate and login user
        if form.is_valid():
            startingAmount = form.cleaned_data["startingAmount"]
            additionalContribution = form.cleaned_data["additionalContribution"]
            additionalContributionFrequency = form.cleaned_data["additionalContributionFrequency"]
            rateOfReturn = form.cleaned_data["rateOfReturn"]
            yearsToGrow = form.cleaned_data["yearsToGrow"]

            baseUrl = reverse("index")
            urlParams = urlencode({
                "starting-amount": startingAmount,
                "additional-contribution": additionalContribution,
                "additional-contribution-frequency": additionalContributionFrequency,
                "rate-of-return": rateOfReturn,
                "years-to-grow": yearsToGrow
            })
            url = "{}?{}".format(baseUrl, urlParams)
            return redirect(url)

    return render(request, "calculator/index.html", {
        "form": form,
        "data": data,
        "investment_worth": investmentWorth,
    })


def resultsData(request):
    try:
        startingAmount = int(request.GET["starting-amount"])
        additionalContribution = int(request.GET["additional-contribution"])
        additionalContributionFrequency = int(
            request.GET["additional-contribution-frequency"])
        rateOfReturn = int(request.GET["rate-of-return"]) / 100
        yearsToGrow = int(request.GET["years-to-grow"])
    except:
        return JsonResponse({"found": False})

    data = []
    lastYearData = {}

    currentYear = timezone.now().year
    annualContribution = additionalContributionFrequency * additionalContribution
    chosenRate = rateOfReturn / additionalContributionFrequency

    for i in range(yearsToGrow):
        yearData = {}
        yearData["year"] = currentYear+i
        yearData["startingAmount"] = startingAmount
        yearData["totalContributions"] = annualContribution * (i+1)

        lastDateEndBalance = 0
        for j in range(additionalContributionFrequency):

            if j == 0:
                if i == 0:
                    dateEndBalance = startingAmount * \
                        (1 + chosenRate) + additionalContribution
                else:
                    dateEndBalance = lastYearData["endBalance"] * \
                        (1 + chosenRate) + additionalContribution
            else:
                dateEndBalance = lastDateEndBalance * \
                    (1 + chosenRate) + additionalContribution

            lastDateEndBalance = round(dateEndBalance)
        endBalance = lastDateEndBalance

        if i == 0:
            yearData["totalInterestEarned"] = endBalance - \
                startingAmount - annualContribution
        else:
            yearData["totalInterestEarned"] = endBalance - lastYearData["endBalance"] - \
                annualContribution + lastYearData["totalInterestEarned"]

        yearData["endBalance"] = lastDateEndBalance
        lastYearData = yearData

        data.append(yearData)

    return JsonResponse(data, safe=False)


def getDataFromParameters(startingAmount, additionalContribution, additionalContributionFrequency, rateOfReturn, yearsToGrow):
    data = []
    lastYearData = {}

    currentYear = timezone.now().year
    annualContribution = additionalContributionFrequency * additionalContribution
    chosenRate = rateOfReturn / 100 / additionalContributionFrequency

    for i in range(yearsToGrow):
        yearData = {}
        yearData["year"] = currentYear+i
        yearData["startingAmount"] = startingAmount
        yearData["annualContribution"] = annualContribution
        yearData["totalContribution"] = annualContribution * (i+1)

        lastDateEndBalance = 0
        for j in range(additionalContributionFrequency):

            if j == 0:
                if i == 0:
                    dateEndBalance = startingAmount * \
                        (1 + chosenRate) + additionalContribution
                else:
                    dateEndBalance = lastYearData["endBalance"] * \
                        (1 + chosenRate) + additionalContribution
            else:
                dateEndBalance = lastDateEndBalance * \
                    (1 + chosenRate) + additionalContribution

            lastDateEndBalance = round(dateEndBalance)
        endBalance = lastDateEndBalance

        if i == 0:
            yearData["interestEarned"] = endBalance - \
                startingAmount - annualContribution
            yearData["totalInterestEarned"] = yearData["interestEarned"]
        else:
            yearData["interestEarned"] = endBalance - \
                lastYearData["endBalance"] - annualContribution
            yearData["totalInterestEarned"] = yearData["interestEarned"] + \
                lastYearData["totalInterestEarned"]

        yearData["endBalance"] = lastDateEndBalance
        lastYearData = yearData

        data.append(yearData)
    return [data, lastDateEndBalance]
