(function ($) {
    "use strict";

    // 看起來引用一次裡面的參數就不見了
    // jQuery.getScript("assets/js/trytry.js")


    // 就是這行去抓 html 的 id  畫在相對應的位置
    // 1 是 price 2 是 volume
    var ctx = $('#TomTom2');

    const brandPrimary = '#20a8d8'
    const brandSuccess = '#4dbd74'
    const brandInfo = '#63c2de'
    const brandDanger = '#f86c6b'
    const brandyellow = '#FFF700'
    const brandblack = '#000000'
    const brandblue = '#47A8BD'
    const brandmeat = '#FFD4CA'
    const brandbrown = '#6b3900'
    var borderColorArr = [brandSuccess, brandDanger, brandPrimary,
        brandyellow, brandblack, brandblue,
        brandmeat, brandbrown]

    // converHex 這個函數在後面會給出rgba(r,g,b)的字串 讓chart.js使用
    function convertHex(hex, opacity) {
        hex = hex.replace('#', '')
        const r = parseInt(hex.substring(0, 2), 16)
        const g = parseInt(hex.substring(2, 4), 16)
        const b = parseInt(hex.substring(4, 6), 16)

        const result = 'rgba(' + r + ',' + g + ',' + b + ',' + opacity / 100 + ')'
        return result
    }
    // 第一次渲染 直接呼叫下面的 function
    renderChart(ctx);

    //Tmall的renderChart

    function renderChart(canvas) {
        // 這裡去跟後端拿資料
        axios.get(`/TomTom2`)
            .then(function (res) {
                const Data = res.data;
                const X_axis = Data.X_axis;
                var totaldiff = Data.totaldiff;
                var data
                // data要記得用 array包起來不能直接放dictionary進去
                data = [{
                    // 因為這裡是拿Data 裡面的 value 做資料整合所以key沒有被引進來
                    label:'China congestion',
                    backgroundColor: convertHex(brandInfo, 10),//輸出形式 rgb()
                    // 這裡的i總共有幾個阿??
                    borderColor: borderColorArr[2],
                    pointHoverBackgroundColor: '#fff',
                    borderWidth: 2,

                    // 這行決定要畫圖的主要資訊
                    data: totaldiff

                }]
                console.log('Xaxis',X_axis)
                console.log(data)


                var myChart = new Chart(canvas, {

                    type: 'line',
                    data: {
                        // 取出第一個Data的key
                        labels: X_axis,
                        datasets: data

                    },
                    options: {
                        title: {
                            display: true,
                            text: 'Congestion time',
                            fontSize: 20
                        },
                        // 如果要自訂義畫布的大小要把 maintainAspectRatio給關掉
                        maintainAspectRatio: false,
                        legend: {
                            display: true
                        },
                        responsive: true,
                        scales: {
                            xAxes: [{
                                ticks: {
                                    autoSkip: false,
                                    // maxRotation: 90,
                                    minRotation: 60
                                },
                                gridLines: {
                                    drawOnChartArea: false
                                },
                                type: 'time',
                                time: {
                                    unit: 'day'
                                },
                                distribution: 'linear'
                            }],
                            yAxes: [{
                                scaleLabel: {
                                    display: true,
                                    labelString: 'congestion time (min)',
                                    fontStyle: 'bold'
                                },
                                ticks: {
                                    //beginAtZero: true,
                                    maxTicksLimit: 5
                                    //stepSize: Step,
                                    //max: MaxPrice

                                },
                                gridLines: {
                                    display: true
                                }
                            }]
                        },
                        elements: {
                            point: {
                                radius: 2,
                                hitRadius: 10,
                                hoverRadius: 4,
                                hoverBorderWidth: 3
                            }
                        }


                    }
                });
                // console.log(myChart)
            }
                //Todo Tmall量的部分
            );


        //這裡怎麼沒有去相對應的路由拿東西

    }

})(jQuery);

// function random (min, max) {
//   return Math.floor(Math.random() * (max - min + 1) + min)
// }
