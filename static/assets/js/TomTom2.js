(function ($) {
    "use strict";
    //polar chart

    const red = '#c51162'
    const pink = '#aa00ff'
    const purple = '#6200ea'
    const deep_purple = '#304ffe'
    const indigo = '#2962ff'
    const blue = '#0091ea'
    const lightblue = '#00b8d4'
    const cyan = '#00bfa5'
    const teal = '#00c853'
    const green = '#64dd17'
    const lightgreen = '#aeea00'
    const lime = '#ffd600'
    const yellow = '#ffab00'
    const amber = '#ff6d00'
    const orange = '#dd2c00'
    const deep_orange = '#3e2723'
    const lightbrown = '#8d6e63'
    const brown = '#212121'
    const lightbrey = '#90a4ae'
    const brey = '#263238'

    const colorHexArr = [red,pink,purple,deep_purple,indigo,blue,lightblue,cyan,teal,
    green,lightgreen,lime,yellow,amber,orange,deep_orange,lightbrown,brown,lightbrey,brey]
    // 看起來引用一次裡面的參數就不見了
    // jQuery.getScript("assets/js/trytry.js")


    // 就是這行去抓 html 的 id  畫在相對應的位置
    // 1 是 price 2 是 volume
    let ctx1 = document.getElementById('TomTom_US');
    let ctx2 = document.getElementById('TomTom_CH');
    let ctx3 = document.getElementById('TomTom_EU');

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
    const city_list_us = {'new-york':17.81,'los-angeles':12.85,'chicago':7.11,
    'san-francisco':5.78,'washington':5.63,
    'dallas-fort-worth':5.45,'houston':5.18,
    'boston':4.8,'philadelphia':4.63,
    'atlanta':4.15,'seattle':4.13,
    'san-jose':3.71,'miami':3.66,
    'detroit':2.77,'minneapolis':2.76,
    'phoenix':2.65,'san-diego':2.55,
    'denver':2.25,'baltimore':2.13}

    // total 驗算 所有的值加起來有沒有100
    // reduce 就是進行sum的方法 後面跟的東西是標準寫法  (accumulator, currentValue) => accumulator + currentValue;
    // https://developer.mozilla.org/zh-TW/docs/Web/JavaScript/Reference/Global_Objects/Array/Reduce
    // https://stackoverflow.com/questions/51989274/how-to-expand-sub-array-in-array-of-objects

    const total = Object.values(city_list_us).reduce((t, n) => t + n)
    console.log(total) 
    // 這裡畫 polarchart
    
    
    // 各城市佔據比例陣列
    let portionArr = []

    // 城市陣列
    let cityArr = []

    // 顏色陣列
    let colorRgbArr = []
    for ( const len of colorHexArr){
         colorRgbArr.push(
            convertHex(len, 10)
            )
    }
     for (const [key, value] of Object.entries(city_list_us)) {
         portionArr.push(
            value
          )
         cityArr.push(
            key
            )

        }
    // 原本這裡要畫圓餅圖的

    // var ctx = document.getElementById( "polarChart" );
    // ctx.height = 150;
    // var myChart = new Chart( ctx, {
    //     type: 'pie',
    //     data: {
    //         datasets: [ {
    //             data:portionArr,
    //             backgroundColor: colorHexArr

    //                         } ],
    //         labels: cityArr
    //     },
    //     options: {
    //         responsive: true,
    //         legend: {
    //                  display: false
    //             },

    //         title: {
    //             display: true,
    //             text:'US GDP Composition',
    //             fontSize: 20
    //             },
    //         // 關於滑過後的 顯示
    //         tooltips: {
    //             callbacks: {
    //                 label: function (tooltipItem, data) {
    //                     var dataset = data.datasets[tooltipItem.datasetIndex];
    //                     //計算總和
    //                     var sum = dataset.data.reduce(function (previousValue, currentValue, currentIndex, array) {
    //                         return previousValue + currentValue;
    //                     });
    //                     var currentValue = dataset.data[tooltipItem.index];
    //                     var percent = Math.round(((currentValue / sum) * 100));
    //                     return " " + data.labels[tooltipItem.index] + ":" + currentValue + " (" + percent + " %)";
    //                 }
    //             }
    //         },

    //     }
    // } );



    // 第一次渲染 直接呼叫下面的 function 引數分別是:
    // "國家", "HTML tag", "顏色陣列裡要用哪個顏色", "標題要放什麼"
    renderChart('USA',ctx1,0,'US congestion');
    renderChart('EU',ctx2,2,'Euro congestion');
    renderChart('CHN',ctx3,4,'China congestion');

    //Tmall的renderChart

    function renderChart(region,canvas,color,title) {
        // 這裡去跟後端拿資料
        axios.get(`/TomTom?region=${region}`)
            .then(function (res) {
                const Data = res.data;
                // console.log(typeof Data)
                const X_axis = Data.X_axis;
                const totaldiff = Data.totaldiff;
                var datasetting
                // data要記得用 array包起來不能直接放dictionary進去
                datasetting = [{
                    // 因為這裡是拿Data 裡面的 value 做資料整合所以key沒有被引進來
                    label: title,
                    backgroundColor: convertHex(brandInfo, 10),//輸出形式 rgb()
                    // 這裡的i總共有幾個阿??
                    borderColor: borderColorArr[color],
                    pointHoverBackgroundColor: '#fff',
                    borderWidth: 2,

                    // 這行決定要畫圖的主要資訊
                    data: totaldiff

                }]
                canvas.height = 400
                // console.log('Xaxis',X_axis)

                var myChart = new Chart(canvas, {

                    type: 'line',
                    // 這行的 data 是這個 js.Chart 物件裡已經定義好的
                    data: {
                        // 取出第一個Data的key
                        labels: X_axis,

                        // 這裡的datasets 裡面就是要放 我們前面把一堆東西放進去的地方
                        datasets: datasetting

                    },
                    options: {
                        title: {
                            display: true,
                            text: title,
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
                                radius: 0,
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
