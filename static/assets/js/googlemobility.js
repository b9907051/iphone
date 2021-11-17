(function ($) {
    "use strict";

    // 看起來引用一次裡面的參數就不見了
    // jQuery.getScript("assets/js/trytry.js")


    // 就是這行去抓 html 的 id  畫在相對應的位置
    // 1 是 price 2 是 volume

    // var ctx1 = $('#google_US');
    // var ctx2 = $('#google_CA');
    // var ctx3 = $('#google_DE');
    // var ctx4 = $('#google_JP');

    // var ctx5 = $('#google_GB');
    // var ctx6 = $('#google_IT');
    // var ctx7 = $('#google_ES');
    // var ctx8 = $('#google_FR');

    // var ctx9 = $('#google_BR');
    // var ctx10 = $('#google_IN');
    // var ctx11 = $('#google_TW');
    // var ctx12 = $('#google_RU');


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
    // 第一次渲染 直接呼叫下面的 function 引數分別是:
    // "國家", "HTML tag", "顏色陣列裡要用哪個顏色", "標題要放什麼"
    // renderChart('US',ctx1);
    // renderChart('CA',ctx2);
    // renderChart('DE',ctx3);
    // renderChart('JP',ctx4);
    // renderChart('GB',ctx5);
    // renderChart('IT',ctx6);
    // renderChart('ES',ctx7);
    // renderChart('FR',ctx8);
    // renderChart('BR',ctx9);
    // renderChart('IN',ctx10);
    // renderChart('TW',ctx11);
    // renderChart('RU',ctx12);

    const countrylist = ['US','CA','DE','JP','GB','IT','ES','FR','BR','IN','TW','RU']
    for (const len in countrylist){
    renderChart(countrylist[len], $('#google_'+countrylist[len]))
    // console.log('[len]',countrylist[len],'obj','#google_'+countrylist[len])
    }

    function renderChart(country, canvas) {
        axios.get(`/google-mobility-trend?country=${country}`)

            .then(function (res) {

                // 這裡 axios 去後端拿的 data 必須要沒有nan 不然拿回來不會是object
                const Data = res.data[country];
                // console.log(typeof Data)
                // console.log(res.data)
                // 這裡把data的key, 在google的檔案裡就是國家 ex:US,JP 傳到 map函數的 k 

                // 把後端拿到的json : {US:{xaxis:[...],parks:[....],..},JP:{xaxis:[...],parks:[....]}....
                // 拆開成一個一個dictionary 用陣列包著, 每個陣列裡的資訊是原本的key 對應到 該key對應到的data
                // 0: US:{'X_axis':[....],'grocery_and_pharmacy':[.....],'parks':[....]}
                // 1: JP:{'X_axis':[....],'grocery_and_pharmacy':[.....],'parks':[....]}

                                // .map(k => ({ [k]: Data[k] }));
                
                const X_axis = res.data['X_axis'];
                // const workplaces = Data.workplace;
                // const residential = Data.residential;
                // console.log('[DATA]',Data[country])
                const Xmax =  X_axis.slice(-1)
                // 把後端拿到的json : {JP:{residential:[...],workplaces:[....],..}
                // 拆開成一個一個dictionary 用陣列包著, 每個陣列裡的資訊是原本的key 對應到 該key對應到的data

                const data_set = Object.keys(Data).map(k => ({ [k]: Data[k] }));
                // console.log('[last data]',X_axis.slice(-1))
                var data_for_plot
// 
                data_for_plot = Object.values(data_set).map((d, i) => ({
                    // 因為這裡是拿Data 裡面的 value 做資料整合所以key沒有被引進來
                    label: Object.keys(d)[0],
                    backgroundColor: convertHex(brandInfo, 10),//輸出形式 rgb()
                    // 這裡的i總共有幾個阿??
                    borderColor: borderColorArr[i],
                    pointHoverBackgroundColor: '#fff',
                    borderWidth: 2,

                    // 這行決定要畫圖的主要資訊
                    data: d[Object.keys(d)[0]]

                }))

                console.log('[data_for_plot]',data_for_plot)
                console.log('[X_axis]',X_axis)

                var myChart = new Chart(canvas, {
                    type: 'line',
                    data: {
                        // 取出第一個Data的key
                        labels: X_axis,
                        datasets: data_for_plot
                    },
                    options: {
                        plugins: {
                            title: {
                              display: true,
                              text: country.concat('  Mobility-Trend') ,
                                  font: {
                                    size: 18
                                  }
                            }
                        },
                        radius: 1,
                        // 如果要自訂義畫布的大小要把 maintainAspectRatio給關掉
                        maintainAspectRatio: false,
                        scales: {
                            x: {
                                type: 'time',
                                ticks:{
                                    stepSize:50
                                },
                                    time: {
                                          unit: 'day',
                                          stepSize:10
                                    },
                            }
                        },
                        elements: {
                            PointElement: {
                                radius: 1,
                                hitRadius: 10,
                                hoverRadius: 4,
                                hoverBorderWidth: 3
                            }
                        }
                    }
                        
                })
            });

                // var myChart = new Chart(canvas, {

                //     type: 'line',
                //     data: {
                //         // 取出第一個Data的key
                //         labels: X_axis,
                //         datasets: data_for_plot
                //     },
                //     options: {
                //         title: {
                //             display: true,
                //             // 
                //             text: 'country',
                //             fontSize: 20
                //         },
                //         // 如果要自訂義畫布的大小要把 maintainAspectRatio給關掉
                //         maintainAspectRatio: false,
                //         plugins: {
                //                   legend: {
                //                     position: 'top',
                //                   }
                //               },

                //         responsive: true,
                //         scales: {
                //             xAxes: [{
                //                 ticks: {
                //                     align: 'end',
                //                     autoSkip: false,
                //                     // maxRotation: 90,
                //                     minRotation: 60,
                //                     // max: Xmax,
                //                 },
                //                 gridLines: {
                //                     drawOnChartArea: false
                //                 },
                //                 type: 'time',
                //                 time: {
                //                     unit: 'day',
                //                     unitStepSize: 20,
                //                 },

                //                 distribution: 'linear'
                //             }],
                //             yAxes: [{
                //                 scaleLabel: {
                //                     display: true,
                //                     labelString: 'percentage',
                //                     fontStyle: 'bold'
                //                 },
                //                 ticks: {
                //                     beginAtZero: true,
                //                     maxTicksLimit: 5,

                //                 },
                //                 gridLines: {
                //                     display: true
                //                 }
                //             }]
                //         },
                //         elements: {
                //             point: {
                //                 radius: 0,
                //                 hitRadius: 10,
                //                 hoverRadius: 4,
                //                 hoverBorderWidth: 3
                //             }
                //         }


                //     }
                // });
                // console.log(myChart)
            }
                //Todo Tmall量的部分

})(jQuery);

// function random (min, max) {
//   return Math.floor(Math.random() * (max - min + 1) + min)
// }
