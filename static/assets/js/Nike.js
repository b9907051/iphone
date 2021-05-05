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

    const productlist = ['Clothes','Shoes']
    for (const len in productlist){
    renderChart(productlist[len], $('#nike_'+productlist[len]))
    // console.log('[len]',productlist[len],'obj','#google_'+productlist[len])
    }

    function renderChart(product, canvas) {
        axios.get(`/Nike?product=${product}`)

            .then(function (res) {

                // 這裡 axios 去後端拿的 data 必須要沒有nan 不然拿回來不會是object
                const Data = res.data[product];
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
                // console.log('[DATA]',Data[product])
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
                              text: product ,
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
                                          stepSize:20
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

            }
                //Todo Tmall量的部分

})(jQuery);

// function random (min, max) {
//   return Math.floor(Math.random() * (max - min + 1) + min)
// }
