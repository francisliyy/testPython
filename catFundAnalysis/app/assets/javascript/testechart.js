import React from 'react';
import ReactDOM from 'react-dom';
import $ from 'jquery';
import echarts from 'echarts';


//cntbnd_jul11.geojsonvar echarts = require('echarts');

// initialize echarts instance with prepared DOM
var myChart = echarts.init(document.getElementById('app'));
// draw chart
myChart.setOption({
    title: {
        text: 'ECharts entry example'
    },
    tooltip: {},
    xAxis: {
        data: ['shirt', 'cardign', 'chiffon shirt', 'pants', 'heels', 'socks']
    },
    yAxis: {},
    series: [{
        name: 'sales',
        type: 'bar',
        data: [5, 20, 36, 10, 10, 20]
    }]
});

var countyChart = echarts.init(document.getElementById('county'));

$.get('/static/assets/map/county.geojson', function (usaJson) {
    countyChart.hideLoading();

    echarts.registerMap('USA', usaJson, {
    });
    var option = {
        title: {
            text: 'Florida Hurrican Losses (2017)',
            subtext: '',
            sublink: '',
            left: 'right'
        },
        tooltip: {
            trigger: 'item',
            showDelay: 0,
            transitionDuration: 0.2,
            formatter: function (params) {
                var value = (params.value + '').split('.');
                value = value[0].replace(/(\d{1,3})(?=(?:\d{3})+(?!\d))/g, '$1,');
                return params.seriesName + '<br/>' + params.name + ': ' + value;
            }
        },
        visualMap: {
            left: 'right',
            min: 500000,
            max: 38000000,
            inRange: {
                color: ['#313695', '#4575b4', '#74add1', '#abd9e9', '#e0f3f8', '#ffffbf', '#fee090', '#fdae61', '#f46d43', '#d73027', '#a50026']
            },
            text:['High','Low'],           // 文本，默认为数值文本
            calculable: true
        },
        toolbox: {
            show: false,
            //orient: 'vertical',
            left: 'left',
            top: 'top',
            feature: {
                dataView: {readOnly: false},
                restore: {},
                saveAsImage: {}
            }
        },
        series: [
            {
                name: 'USA PopEstimates',
                type: 'map',
                roam: true,
                map: 'USA',
                itemStyle:{
                    emphasis:{label:{show:true}}
                },
                // 文本位置修正
                textFixed: {
                },
                data:[
                ]
            }
        ]
    };

    countyChart.setOption(option);
});
                    