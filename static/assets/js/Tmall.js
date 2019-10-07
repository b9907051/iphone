( function ( $ ) {
    "use strict";


const brandPrimary = '#20a8d8'
const brandSuccess = '#4dbd74'
const brandInfo = '#63c2de'
const brandDanger = '#f86c6b'
const brandyellow = '#FFF700'
const brandblack = '#000000'

function convertHex (hex, opacity) {
  hex = hex.replace('#', '')
  const r = parseInt(hex.substring(0, 2), 16)
  const g = parseInt(hex.substring(2, 4), 16)
  const b = parseInt(hex.substring(4, 6), 16)

  const result = 'rgba(' + r + ',' + g + ',' + b + ',' + opacity / 100 + ')'
  return result
}

function random (min, max) {
  return Math.floor(Math.random() * (max - min + 1) + min)
}
    fetch('/Tmall')
      .then(function(response) {
        return response.json();
      }).then(function(Data) {


    const Cellphone = Object.keys(Data)
      .filter(k => k !== 'MaxDealnumber' && k !== 'X_axis')
      .map(k => ({ [k]: Data[k] }));
    const MaxDealnumber = Data.MaxDealnumber;
    const X_axis = Data.X_axis;

    // 另一個解法
    // let MaxDealnumber = Data.MaxDealnumber;
    // let X_axis = Data.X_axis;
    // then remove it from the object
    // delete(Data.MaxDealnumber);
    // delete(Data.X_axis);
    // the remaining keys are cellphones
    // console.log(maxValue)

    // map(d,i) 就是把 data跟 index 併在一起,是固定寫法
    // values(Data) = {dealnumber:[],Timestemp:[]}

    // ex:
    // data = Object.values(obj).map(d => d.dealnumber)
    // data = [[1,2,3], [4,6,7]]
    // console.log(Data)
    var borderColorArr = [brandSuccess,brandDanger,brandPrimary,brandyellow,brandblack]

    var data,time,dealnumber;

    data = Object.values(Cellphone).map((d, i) => ({
        // 因為這裡是拿Data 裡面的 value 做資料整合所以key沒有被引進來
        label: Object.keys(d)[0],
        backgroundColor: convertHex(brandInfo, 10),//輸出形式 rgb()
        // 這裡的i總共有幾個阿??
        borderColor: borderColorArr[i],
        pointHoverBackgroundColor: '#fff',
        borderWidth: 2,
        data: d[Object.keys(d)[0]].Dealnumber
    }))

    //舊的寫法
    // data = Object.values(Data).map((d, i) => ({
    //     // 因為這裡是拿Data 裡面的 value 做資料整合所以key沒有被引進來
    //     label: Object.keys(Data)[i],
    //     backgroundColor: convertHex(brandInfo, 10),//輸出形式 rgb()
    //     // 這裡的i總共有幾個阿??
    //     borderColor: borderColorArr[i],
    //     pointHoverBackgroundColor: '#fff',
    //     borderWidth: 2,
    //     data: d.Dealnumber
    // }))
    
    // time = Object.values(Data).map(d => d.Timestemp)
    // dealnumber = Object.values(Data).map(d => d.Dealnumber)

    // 這行要把dealnumber的array展開 [[flatten an array of arrays]
    // var dealnumberstrArr = []

    // for(var i = 0; i < dealnumber.length; i++)
    // {
    //   dealnumberstrArr = dealnumberstrArr.concat(dealnumber[i]);
    // }

    // // 把dealnumber 轉換成int併再一起
    // var dealnumberintArr = dealnumberstrArr.map(function(item) {
    // return parseInt(item, 10);
    // });

    // var Maxdealnumber = Math.max.apply(null,dealnumberintArr) + 2000

    //Traffic Chart
    var ctx = document.getElementById( "Tmall" );
    //ctx.height = 200;
    var myChart = new Chart( ctx, {
        type: 'line',
        data: {
          // 取出第一個Data的key
          labels: X_axis,
          datasets:data

        },
        options: {

            maintainAspectRatio: true,
            legend: {
                display: true
            },
            responsive: true,
            title: {
                display: true,
                text: '天貓交易資訊',
                fontSize:20
            },
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
                  type:'time',
                  time:{
                    unit:'day'
                  }
                }],
                yAxes: [ {
                      ticks: {
                        beginAtZero: true,
                        maxTicksLimit: 5,
                        stepSize: 5000,
                        max: MaxDealnumber
                      },
                      scaleLabel: {
                        display: true,
                        labelString: '月銷售量',
                        fontStyle:'bold'
                      },
                      gridLines: {
                        display: true
                      }
                } ]
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
    } );

    });


} )( jQuery );