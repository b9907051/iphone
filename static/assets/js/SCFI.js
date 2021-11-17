(function ($) {
    "use strict";

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
        brandblack, brandblue,
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

    const index_list = ['East','West','Europe','SCFI']
    const title_list = ['美東','美西','歐洲','SCFI指數']
    for (const len in index_list){
    renderChart(index_list[len], $('#'+index_list[len]), len,title_list[len])
    // console.log('[len]',productlist[len],'obj','#google_'+productlist[len])
    }


    function renderChart(index, canvas, color, title_list) {
        axios.get(`/SCFI?index=${index}`)

            .then(function (res) {
                const Data = res.data;
                // 這裡 axios 去後端拿的 data 必須要沒有nan 不然拿回來不會是object
                const price = Data.Index;
                // console.log(typeof Data)
                // 這裡把data的key, 在google的檔案裡就是國家 ex:US,JP 傳到 map函數的 k 

                // 把後端拿到的json : {US:{xaxis:[...],parks:[....],..},JP:{xaxis:[...],parks:[....]}....
                // 拆開成一個一個dictionary 用陣列包著, 每個陣列裡的資訊是原本的key 對應到 該key對應到的data
                // 0: US:{'X_axis':[....],'grocery_and_pharmacy':[.....],'parks':[....]}
                // 1: JP:{'X_axis':[....],'grocery_and_pharmacy':[.....],'parks':[....]}

                                // .map(k => ({ [k]: Data[k] }));
                // console.log(Data)
                const X_axis = Data.X_axis;
                // const workplaces = Data.workplace;
                // const residential = Data.residential;
                // console.log('[DATA]',Data[datasource])

                // 把後端拿到的json : {JP:{residential:[...],workplaces:[....],..}
                // 拆開成一個一個dictionary 用陣列包著, 每個陣列裡的資訊是原本的key 對應到 該key對應到的data

                const datasetting = [{
                    // 因為這裡是拿Data 裡面的 value 做資料整合所以key沒有被引進來
                    label: index,
                    backgroundColor: convertHex(brandInfo, 10),//輸出形式 rgb()
                    // 這裡的i總共有幾個阿??
                    borderColor: borderColorArr[color],
                    pointHoverBackgroundColor: '#fff',
                    borderWidth: 2,

                    // 這行決定要畫圖的主要資訊
                    data: price

                }]
                console.log('[Data]',datasetting)
                console.log('[X_axis]',X_axis)

                // canvas[1] = week[1] or day[1] 去對應 html 的 label
                // period2ctx = {
                //  week: { 1: ctx1_week, 2: ctx2_week },
                //  day: { 1: ctx1_day, 2: ctx2_day }
                // }
                canvas[0].height = 400
                var myChart = new Chart(canvas, {

                    type: 'line',
                    data: {
                        // 取出第一個Data的key
                        labels: X_axis,
                        datasets: datasetting

                    },
                    options: {
                        plugins: {
                            title: {
                              display: true,
                              text: title_list,
                                  font: {
                                    size: 30
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
                                ticks: {
                                    align: 'end',
                                    autoSkip: false,
                                    // maxRotation: 90,
                                    minRotation: 30,
                                    // max: Xmax,
                                },
                                gridLines: {
                                    drawOnChartArea: false
                                },


                                distribution: 'linear'
                            },
                            y: {
                                display: true,
                                title: {
                                  display: true,
                                  text: 'Price'
                                },
                                gridLines: {
                                    display: true
                                }
                            }
                        },
                        elements: {
                            point: {
                                radius: 0,
                                hitRadius: 10,
                                hoverRadius: 4,
                                hoverBorderWidth: 3
                            },
                            line:{
                                borderWidth: 10
                            }
                        }


                    }
                });
                // console.log(myChart)
            }
                //Todo Tmall量的部分
            )};
})(jQuery);

// function random (min, max) {
//   return Math.floor(Math.random() * (max - min + 1) + min)
// }
