document.addEventListener("DOMContentLoaded", function () {
    let state = {
        "years": [],
        "startingAmount": [],
        "totalContributions": [],
        "totalInterestEarned": [],
    }

    let lastState = {}

    fetch(`/data${window.location.search}`)
        .then(response => response.json())
        .then(data => {
            for (let i = 0; i < data.length; i++) {
                state.years.push(data[i].year)
                state.startingAmount.push(data[i].startingAmount)
                state.totalContributions.push(data[i].totalContributions)
                state.totalInterestEarned.push(data[i].totalInterestEarned)
                if (i == data.length - 1) {
                    lastState.years = data[i].year
                    lastState.startingAmount = data[i].startingAmount
                    lastState.totalContributions = data[i].totalContributions
                    lastState.totalInterestEarned = data[i].totalInterestEarned
                }
            }

            let chartGrowthData = {
                "type": "bar",
                "plot": {
                    stacked: true,
                    "stack-type": "normal"
                },
                "legend": {
                    "x": "10%",
                    "y": "0%"
                },
                "scale-x": {
                    "values": state.years
                },
                "series": [
                    {
                        values: state.startingAmount,
                        stack: 1,
                        text: `Starting Amount (€${lastState.startingAmount})`
                    },
                    {
                        values: state.totalContributions,
                        stack: 1,
                        text: `Total Contributions (€${lastState.totalContributions})`
                    },
                    {
                        values: state.totalInterestEarned,
                        stack: 1,
                        text: `Total Interest Earned (€${lastState.totalInterestEarned})`
                    },
                ]
            }

            let totalMoneyData = {
                "type": "pie",
                "legend": {

                },
                "series": [
                    {
                        values: [lastState.startingAmount],
                        text: `Starting Amount (€${lastState.startingAmount})`
                    },
                    {
                        values: [lastState.totalContributions],
                        text: `Total Contributions (€${lastState.totalContributions})`
                    },
                    {
                        values: [lastState.totalInterestEarned],
                        text: `Total Interest Earned (€${lastState.totalInterestEarned})`
                    },
                ]
            }

            zingchart.render({
                id: "growth-chart",
                data: chartGrowthData,
            })

            zingchart.render({
                id: "total-money-chart",
                data: totalMoneyData,
            })
        });

    console.log(state)


});