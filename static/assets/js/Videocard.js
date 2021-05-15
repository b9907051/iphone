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
        brandblack, brandblue, brandyellow, 
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
    const productlist = ['RTX-3060','RTX-3080','RTX-3070','GTX-1060']
    const launchPrice = [399,699,499,299]
    for (const len in productlist){
    renderChart(productlist[len], $('#'+productlist[len]),len, launchPrice[len])
    // console.log('[len]',productlist[len],'obj','#google_'+productlist[len])
    }


    //Tmall的renderChart

    function renderChart(product,canvas,color,launchPrice) {
        // 這裡去跟後端拿資料
        axios.get(`/Videocard?product=${product}`)
            .then(function (res) {
                const Data = res.data;
                // console.log(typeof Data)
                const X_axis = Data.X_axis;
                const price = Data.price;
                var datasetting
                // data要記得用 array包起來不能直接放dictionary進去
                datasetting = [{
                    // 因為這裡是拿Data 裡面的 value 做資料整合所以key沒有被引進來
                    label: product,
                    backgroundColor: convertHex(brandInfo, 10),//輸出形式 rgb()
                    // 這裡的i總共有幾個阿??
                    borderColor: borderColorArr[color],
                    pointHoverBackgroundColor: '#fff',
                    borderWidth: 2,

                    // 這行決定要畫圖的主要資訊
                    data: price

                }]
                console.log(datasetting)
                // 這裡的 canvas 是陣列, 在TomTom2js 裡面不是這樣宣告的所以不用加上[0]
                canvas[0].height = 400
                // console.log('Xaxis',X_axis)
                const annotation1 = {
                  type: 'line',
                  scaleID: 'y',
                  borderWidth: 3,
                  borderColor: 'black',
                  value: launchPrice,
                  label: {
                    content: 'launchPrice:'+launchPrice,
                    enabled: true
                  },
                };

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
                        type: 'line',
                        data: {
                            // 取出第一個Data的key
                            labels: X_axis,
                            datasets: datasetting
                        },
                        plugins: {
                            title: {
                                display: true,
                                text: 'Product:' + product,
                                fontSize: 20
                            },
                            annotation: {
                                annotations: {
                                  annotation1
                                }
                            }
                        },

                        // 如果要自訂義畫布的大小要把 maintainAspectRatio給關掉
                        maintainAspectRatio: false,
                        legend: {
                            display: true
                        },
                        responsive: true,
                        scales: {
                            x: {
                                type: 'time',
                                // ticks:{
                                //     stepSize:50
                                // },
                                time: {
                                      unit: 'day',
                                      stepSize:10,
                                      tooltipFormat:'yyyy-MM-dd'
                                },
                            },

                            y: {
                                display: true,
                                // beginAtZero:false,
                                title: {
                                  display: true,
                                  text: 'percentage'
                                }
                            }
                        },
                        elements: {
                            point: {
                                radius: 1,
                                hitRadius: 10,
                                hoverRadius: 3,
                                hoverBorderWidth: 3
                            }
                        },


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
