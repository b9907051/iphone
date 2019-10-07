(function ($) {
	"use strict";

	// 看起來引用一次裡面的參數就不見了
	// jQuery.getScript("assets/js/trytry.js")


	// 就是這行去抓 html 的 id  畫在相對應的位置
	var ctx1_day = $('#Zhongguancun_day');
	var ctx2_day = $('#Tmall_day');
	var ctx1_week = $('#Zhongguancun_week');
	var ctx2_week = $('#Tmall_week')



	var period2ctx = {
		week: { 1: ctx1_week, 2: ctx2_week },
		day: { 1: ctx1_day, 2: ctx2_day }
	}
	const brandPrimary = '#20a8d8'
	const brandSuccess = '#4dbd74'
	const brandInfo = '#63c2de'
	const brandDanger = '#f86c6b'
	const brandyellow = '#FFF700'
	const brandblack = '#000000'

	function convertHex(hex, opacity) {
		hex = hex.replace('#', '')
		const r = parseInt(hex.substring(0, 2), 16)
		const g = parseInt(hex.substring(2, 4), 16)
		const b = parseInt(hex.substring(4, 6), 16)

		const result = 'rgba(' + r + ',' + g + ',' + b + ',' + opacity / 100 + ')'
		return result
	}
	// 第一次渲染 直接呼叫下面的 function
	renderChart('week', period2ctx['week']);

	// TODO: 天貓的第一次渲染
	// renderChart()
	// 接著的渲染都要按了按鍵以後
	$(document).ready(function () {
		//去接 class = tab 的點擊事件
		$(".tab").click(function () {
			const timePeriod = $(this).attr('timeperiod');

			console.log('[timePeriod]', timePeriod);
			// 中關村的畫圖
			renderChart(timePeriod, period2ctx[timePeriod]);
			//TODO: 天貓的畫圖
		})

	});

	// TODO: 天貓的renderChart

	function renderChart(timePeriod, canvas) {
		axios.get(`/api?timeperiod=${timePeriod}`)
			.then(function (res) {
				const Data = res.data;
				console.log('[DATA]', Data)
				const Cellphone = Object.keys(Data)
					.filter(k => k !== 'Max_info' && k !== 'X_axis')
					.map(k => ({ [k]: Data[k] }));
				const MaxPrice = Data.Max_info;
				const X_axis = Data.X_axis;

				var borderColorArr = [brandSuccess, brandDanger, brandPrimary, brandyellow, brandblack]

				var data, time, dealnumber;

				data = Object.values(Cellphone).map((d, i) => ({
					// 因為這裡是拿Data 裡面的 value 做資料整合所以key沒有被引進來
					label: Object.keys(d)[0],
					backgroundColor: convertHex(brandInfo, 10),//輸出形式 rgb()
					// 這裡的i總共有幾個阿??
					borderColor: borderColorArr[i],
					pointHoverBackgroundColor: '#fff',
					borderWidth: 2,
					data: d[Object.keys(d)[0]].Price
				}))

				//如果 myChart 之前有產生過的話先把他給刪掉等夏畫
				if (myChart != undefined) {
					console.log('destroy')
					myChart.destroy();
				}
				var myChart = new Chart(canvas[1], {
					type: 'line',
					data: {
						// 取出第一個Data的key
						labels: X_axis,
						datasets: data

					},
					options: {
						title: {
							display: true,
							text: '中關村銷售資訊',
							fontSize: 20
						},

						maintainAspectRatio: true,
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
									unit: 'week'
								},
								distribution: 'series'
							}],
							yAxes: [{
								scaleLabel: {
									display: true,
									labelString: '價格',
									fontStyle: 'bold'
								},
								ticks: {
									beginAtZero: true,
									maxTicksLimit: 5,
									stepSize: 500,
									max: MaxPrice
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
			});
		axios.get(`/Tmall?timeperiod=${timePeriod}`)
			.then(function (res) {
				const Data = res.data;
				console.log('[DATA]', Data)
				const Cellphone = Object.keys(Data)
					.filter(k => k !== 'Max_info' && k !== 'X_axis')
					.map(k => ({ [k]: Data[k] }));
				const MaxDealnumber = Data.Max_info;
				const X_axis = Data.X_axis;

				var borderColorArr = [brandSuccess, brandDanger, brandPrimary, brandyellow, brandblack]

				var data, time, dealnumber;

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
				console.log(data)
				//如果 myChart2 之前有產生過的話先把他給刪掉等夏畫
				if (myChart2 != undefined) {
					console.log('destroy')
					myChart2.destroy();
				}
				var myChart2 = new Chart(canvas[2], {
					type: 'line',
					data: {
						// 取出第一個Data的key
						labels: X_axis,
						datasets: data

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
							fontSize: 20
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
								type: 'time',
								time: {
									unit: 'day'
								}
							}],
							yAxes: [{
								ticks: {
									beginAtZero: true,
									maxTicksLimit: 5,
									stepSize: 5000,
									max: MaxDealnumber
								},
								scaleLabel: {
									display: true,
									labelString: '月銷售量',
									fontStyle: 'bold'
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
			});

		//這裡怎麼沒有去相對應的路由拿東西

	}






})(jQuery);

// function random (min, max) {
//   return Math.floor(Math.random() * (max - min + 1) + min)
// }
