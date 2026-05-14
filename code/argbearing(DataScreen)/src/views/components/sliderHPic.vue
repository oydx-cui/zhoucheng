<template>
    <slider ref="slider" :options="options" @slide='slide' @tap='onTap' @init='onInit'>
        <slideritem v-for="(item, index) in someList" :key="index" :style="item.style" class="slider-item">
            <div class="slider-content">
                <img :src="item.image" alt="Slider Image" class="slider-image">
                <span class="bearing-number">Bearing-{{ item.bearingNumber }}</span>
            </div>
            <div :ref="'echartsContainer' + index" class="echarts-container"></div>
        </slideritem>
        <div slot="loading">加载中...</div>
    </slider>
</template>

<script>
import { slider, slideritem } from 'vue-concise-slider'
import echarts from 'echarts'

export default {
    props: {
        data: Object
    },
    data() {
        return {
            someList: [
                {
                    image: require('@/assets/images/bearing.png'),
                    style: {
                        'width': '49%',
                        'margin-right': '2%'
                    },
                    bearingNumber: 1,
                    pointData: []
                },
                {
                    image: require('@/assets/images/bearing.png'),
                    style: {
                        'width': '49%',
                        'margin-right': '2%'
                    },
                    bearingNumber: 2,
                    pointData: []
                },
                {
                    image: require('@/assets/images/bearing.png'),
                    style: {
                        'width': '49%',
                        'margin-right': '2%'
                    },
                    bearingNumber: 3,
                    pointData: []
                },
                {
                    image: require('@/assets/images/bearing.png'),
                    style: {
                        'width': '49%',
                        'margin-right': '2%'
                    },
                    bearingNumber: 4,
                    pointData: []
                },
                {
                    image: require('@/assets/images/bearing.png'),
                    style: {
                        'width': '49%',
                        'margin-right': '2%'
                    },
                    bearingNumber: 5,
                    pointData: []
                },
                {
                    image: require('@/assets/images/bearing.png'),
                    style: {
                        'width': '49%',
                        'margin-right': '2%'
                    },
                    bearingNumber: 6,
                    pointData: []
                },
                {
                    image: require('@/assets/images/bearing.png'),
                    style: {
                        'width': '49%',
                        'margin-right': '2%'
                    },
                    bearingNumber: 7,
                    pointData: []
                },
                {
                    image: require('@/assets/images/bearing.png'),
                    style: {
                        'width': '49%',
                        'margin-right': '2%'
                    },
                    bearingNumber: 8,
                    pointData: []
                },
                {
                    image: require('@/assets/images/bearing.png'),
                    style: {
                        'width': '49%',
                        'margin-right': '2%'
                    },
                    bearingNumber: 9,
                    pointData: []
                },
                {
                    image: require('@/assets/images/bearing.png'),
                    style: {
                        'width': '49%',
                        'margin-right': '2%'
                    },
                    bearingNumber: 10,
                    pointData: []
                },
                {
                    image: require('@/assets/images/bearing.png'),
                    style: {
                        'width': '49%',
                        'margin-right': '2%'
                    },
                    bearingNumber: 11,
                    pointData: []
                },
                {
                    image: require('@/assets/images/bearing.png'),
                    style: {
                        'width': '49%',
                        'margin-right': '2%'
                    },
                    bearingNumber: 12,
                    pointData: []
                }
            ],
            options: {
                limitMoveNum: 3,
                currentPage: 0,
                tracking: false,
                slidesToScroll: 1,
                autoplay: 3500,
                loop: true,
                loopedSlides: 2,
                speed: 1000,
            },
            faultLocMapping: {
                '0': [52, 80],
                '1': [36, 36],
                '2': [80, 50],
                '3': [52, 12]
            },
            faultLocs: [],
            faultDias: [],
        }
    },
    mounted() {

        this.someList = [];

        this.faultLocs = [];
        this.faultDias = [];

        // 遍历所有的键值对
        Object.keys(this.data).forEach(key => {
            // 获取每个键值对的值部分的最后一个json数据
            const lastData = this.data[key][this.data[key].length - 1];
            let pointDataItem = [];
            let faultLocItem = [];
            let faultDiaItem = [];
            // const faultLocMapping = {
            //     '0': [52, 80],
            //     '1': [36, 36],
            //     '2': [80, 50],
            //     '3': [52, 12]
            // };

            // 检查最后一个json数据的faultDia1是否为'0'，如果不是，则将其faultLoc1映射并添加到pointDataItem中
            if (lastData.faultDia1 !== '0') {
                pointDataItem.push(this.faultLocMapping[lastData.faultLoc1]);
            }
            else pointDataItem.push([]);
            faultLocItem.push(["滚珠", "内圈", "外圈3点钟", "外圈6点钟"][parseInt(lastData.faultLoc1)]);
            faultDiaItem.push(["正常", "7mils", "14mils", "21mils"][parseInt(lastData.faultDia1)]);

            // 检查最后一个json数据的faultDia2是否为'0'，如果不是，则将其faultLoc2映射并添加到pointDataItem中
            if (lastData.faultDia2 !== '0') {
                pointDataItem.push(this.faultLocMapping[lastData.faultLoc2]);
            }
            else pointDataItem.push([]);
            faultLocItem.push(["滚珠", "内圈", "外圈3点钟", "外圈6点钟"][parseInt(lastData.faultLoc2)]);
            faultDiaItem.push(["正常", "7mils", "14mils", "21mils"][parseInt(lastData.faultDia2)]);

            // 检查最后一个json数据的faultDia3是否为'0'，如果不是，则将其faultLoc3映射并添加到pointDataItem中
            if (lastData.faultDia3 !== '0') {
                pointDataItem.push(this.faultLocMapping[lastData.faultLoc3]);
            }
            else pointDataItem.push([]);
            faultLocItem.push(["滚珠", "内圈", "外圈3点钟", "外圈6点钟"][parseInt(lastData.faultLoc3)]);
            faultDiaItem.push(["正常", "7mils", "14mils", "21mils"][parseInt(lastData.faultDia3)]);

            // 将faultLocItem/faultDiaItem添加到faultLocs/faultDias中
            this.faultLocs.push(faultLocItem);
            this.faultDias.push(faultDiaItem);

            this.someList[parseInt(key) - 1] = {};
            this.someList[parseInt(key) - 1].pointData = pointDataItem;

            this.someList[parseInt(key) - 1].image = require('@/assets/images/bearing.png');
            this.someList[parseInt(key) - 1].style = { 'width': '49%', 'margin-right': '2%' };
            this.someList[parseInt(key) - 1].bearingNumber = parseInt(key);

        });

        // 将结果赋给组件的数据属性
        // this.pointData = pointData;
        console.log('pointData1: ', this.someList[0].pointData);
        console.log('someList: ', this.someList);

        // 初始化 ECharts 图表
        this.someList.forEach((item, index) => {
            if (item.pointData) {
                const chartContainer = this.$refs['echartsContainer' + index][0]
                const myChart = echarts.init(chartContainer)
                this.initChart(myChart, item.pointData, index)
            }
        })
    },
    methods: {
        // 初始化 ECharts 图表
        initChart(chart, pointData, index) {
            const option = {
                tooltip: {
                    trigger: 'item',
                    formatter: (params) => {
                        return '故障位置：' + this.faultLocs[index][params.dataIndex] + '<br/>' +
                            '故障直径：' + this.faultDias[index][params.dataIndex] + '<br/>';
                    }
                },
                xAxis: {
                    type: 'value',
                    min: 0,
                    max: 100,
                    show: false
                },
                yAxis: {
                    type: 'value',
                    min: 0,
                    max: 100,
                    show: false
                },
                grid: {
                    show: false
                },
                series: [
                    {
                        type: 'effectScatter',
                        symbolSize: 15,
                        data: pointData,
                        itemStyle: {
                            color: function (params) {
                                var colorList = ['#fe2f2f', '#d86262', '#fdc1c1']
                                if (params.dataIndex <= 2) {
                                    return colorList[params.dataIndex]
                                } else {
                                    return colorList[params.dataIndex % 3]
                                }
                            }
                        },
                        showEffectOn: 'render',
                        hoverAnimation: true,
                        zlevel: 1
                    }
                ]
            }
            chart.setOption(option)
        }
    },
    components: {
        slider,
        slideritem
    }
}
</script>

<style lang="less">
.slider-item {
    position: relative;
    width: 100%;
}

.slider-content {
    position: relative;
    height: 92%;
}

.slider-image {
    width: 80%;
    height: auto;
}

.bearing-number {
    position: absolute;
    bottom: 5px;
    left: 50%;
    transform: translateX(-50%);
    display: inline-block;
    color: #ffffff;
    font-size: 15px;
}

.echarts-container {
    position: absolute;
    top: -28px;
    left: 0;
    width: 300px;
    height: 320px;
    z-index: 1;
}
</style>