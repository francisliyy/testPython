import React from 'react';
import ReactDOM from 'react-dom';
import $ from 'jquery';
import echarts from 'echarts';


let countyChart = echarts.init(document.getElementById('countyHeatChart'));
let countydata = $('#countyHeatChart').data('county');

$.get('/static/assets/map/countygeo.json', function (usaJson) {
    countyChart.hideLoading();

    echarts.registerMap('USA', usaJson, {
    });
    let option = {
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
            formatter: '{b}<br/>{c} (%)'
        },
        visualMap: {
            left: 'right',
            min: 0,
            max: 100,
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
                    normal:{label:{show:true}},
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

    

    let pChange = countydata["Percentage Change"];

    var dataArray = new Array();
    for(var key in pChange) {
        option.series[0].data.push({name:key.toUpperCase(),value:pChange[key].toFixed(2)})
    }

    console.log(option);

    countyChart.setOption(option);
});
                    