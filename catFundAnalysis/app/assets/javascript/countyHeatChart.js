import React from 'react';
import ReactDOM from 'react-dom';
import $ from 'jquery';
import echarts from 'echarts';


let countyChart = echarts.init(document.getElementById('countyHeatChart'));
let countydata = $('#countyHeatChart').data('county');
let tob = $('#countyHeatChart').data('tob').split("_")[1].toUpperCase();
tob = tob === 'LR' ? 'COMMERCIAL' : tob;
let maxValue = $('#countyHeatChart').data('maxvalue')||100;
let minValue = $('#countyHeatChart').data('minvalue')||-100;
let maptype = $('#countyHeatChart').data('maptype');
let jsonfile = '/static/assets/map/'+maptype+'FL.json';


$.get(jsonfile, function (usaJson) {
    countyChart.hideLoading();

    echarts.registerMap('USA', usaJson, {
    });
    let option = {
        /*title: {
            text: 'Florida '+maptype+' Hurrican Losses (2017)',
            subtext: 'Type of Building : '+tob,
            sublink: '',
            left: 'right'
        },*/
        tooltip: {
            trigger: 'item',
            showDelay: 0,
            transitionDuration: 0.2,
            formatter:  function (params,ticket,callback) {
                return params.name+"<br/>"+(params.value||0)+"(%)";                
            },
        },
        visualMap: {
            left: 'left',
            min: minValue,
            max: maxValue,
            inRange: {
                color: ['#313695', '#4575b4', '#74add1', '#abd9e9', '#e0f3f8', '#ffffbf', '#fee090', '#fdae61', '#f46d43', '#d73027', '#a50026']
            },
            //text:['High',''],           // 文本，默认为数值文本
            splitNumber: 10,
            
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
                    //normal:{label:{show:maptype=='County'?true:false}},
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

    

    let pChange = countydata["Total Percentage Change"];

    var dataArray = new Array();
    for(var key in pChange) {
        if(key==='Total') continue;
        //since county name from geojson has no space, so space in csv data should be trimmed 
        option.series[0].data.push({name:key.toUpperCase().replace(/[ ]/g,""),value:parseFloat(pChange[key].toFixed(2))})
    }

    console.log(option);

    countyChart.setOption(option);
});
                    