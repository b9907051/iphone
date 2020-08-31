(function ($) {
	"use strict";

	// 看起來引用一次裡面的參數就不見了
	// jQuery.getScript("assets/js/trytry.js")


	// 就是這行去抓 html 的 id  畫在相對應的位置
	var ctx1_day = $('#1H2020_day');
	// var ctx2_day = $('#Tmall_day');
	var ctx1_week = $('#1H2020_week');
	// var ctx2_week = $('#Tmall_week')



	var period2ctx = {
		week: ctx1_week,
		day: ctx1_day
	}
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
	renderChart('week', period2ctx['week']);

	// TODO: 天貓的第一次渲染
	// renderChart()
	// 接著的渲染都要按了按鍵以後
	// 按了案件以後會觸發 renderChart()函數 並assign timePeriod 標籤的屬性
	$(document).ready(function () {
		//去接 class = tab 的點擊事件
		$(".tab").click(function () {
			const timePeriod = $(this).attr('timeperiod');

			console.log('[timePeriod]', timePeriod);
			// period2ctx['week'] = { 1: ctx1_week, 2: ctx2_week }
			renderChart(timePeriod, period2ctx[timePeriod]);
			//TODO: 天貓的畫圖
		})

	});

	//中關村的renderChart

	function renderChart(timePeriod, canvas) {
		axios.get(`/1H2020?timeperiod=${timePeriod}`)
			.then(function (res) {
				const Data = res.data;
				console.log('[DATA]', Data)
				const Cellphone = Object.keys(Data)
					.filter(k => k !== 'Max_info' && k !== 'X_axis'
						&& k !== 'Main_info' && k !== 'Time_period'
						&& k !== 'Step')
					.map(k => ({ [k]: Data[k] }));
				const MaxPrice = Data.Max_info;
				const X_axis = Data.X_axis;
				var Main_info = Data.Main_info;
				var TimePeriod = Data.Time_period;


				var data, time, dealnumber;
				// => 這個東西是 arrow function. 有點像匿名函數

				data = Object.values(Cellphone).map((d, i) => ({
					// 因為這裡是拿Data 裡面的 value 做資料整合所以key沒有被引進來
					label: Object.keys(d)[0],
					backgroundColor: convertHex(brandInfo, 10),//輸出形式 rgb()
					// 這裡的i總共有幾個阿??
					borderColor: borderColorArr[i],
					pointHoverBackgroundColor: '#fff',
					borderWidth: 2,

					// 這行決定要畫圖的主要資訊
					data: d[Object.keys(d)[0]][Main_info]

				}))

				//如果 myChart 之前有產生過的話先把他給刪掉等夏畫
				if (myChart != undefined) {
					console.log('destroy')
					myChart.destroy();
				}
				// canvas[1] = week[1] or day[1] 去對應 html 的 label
				// period2ctx = {
				// 	week: { 1: ctx1_week, 2: ctx2_week },
				// 	day: { 1: ctx1_day, 2: ctx2_day }
				// }
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
							text: '5G手機銷售資訊',
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
									unit: TimePeriod
								},
								distribution: 'linear'
							}],
							yAxes: [{
								scaleLabel: {
									display: true,
									labelString: Main_info,
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


		//這裡怎麼沒有去相對應的路由拿東西

	}

})(jQuery);

// function random (min, max) {
//   return Math.floor(Math.random() * (max - min + 1) + min)
// }
