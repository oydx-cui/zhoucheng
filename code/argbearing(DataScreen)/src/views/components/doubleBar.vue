<template>
    <div class="chart"></div>
</template>

<style lang="less" scoped>
.chart {
    height: 100%;
}
</style>

<script>
export default {
    name: '',
    props: {
        data: Object
    },
    data() {
        return {}
    },
    methods: {
        setChart() {
            let option = {
                tooltip: {
                    trigger: 'axis',
                    axisPointer: {
                        type: 'shadow'
                    },
                },
                title: {
                    text: this.data.title,
                    top: "5%",
                    left: '5%',
                    textStyle: {
                        color: '#fff',
                        fontSize: 12,
                    }
                },
                legend: {
                    data: [
                        { name: this.data.data[0].name, icon: 'circle' },
                        { name: this.data.data[1].name, icon: 'circle' },
                    ],
                    left: "center",
                    top: "17%",
                    orient: 'horizontal',
                    itemWidth: 7,
                    itemHeight: 7,
                    itemGap: 10,
                    textStyle: {
                        color: '#67C3D6',
                        fontSize: 10
                    }
                },
                grid: {
                    left: "5%",
                    top: '35%',
                    right: '5%',
                    bottom: '15%'
                },
                xAxis: {
                    axisLine: {
                        lineStyle: {
                            color: '#2B427F'
                        }
                    },
                    axisLabel: {
                        color: '#0DF5F8',
                        fontSize: 8,
                        interval: 0,
                    },
                    axisTick: {
                        inside: true,
                        alignWithLabel: true,
                        interval: 0,
                        color: '#2B427F'
                    },
                    data: this.data.xname
                },
                yAxis: [
                    {
                        type: 'value',
                        // name: this.data.data[0].name, // 第一个数据系列的纵坐标轴名称
                        // nameTextStyle: {
                        //     color: this.data.data[0].color // 第一个数据系列的纵坐标轴名称颜色
                        // },
                        axisLine: {
                            lineStyle: {
                                color: this.data.data[0].color // 第一个数据系列的纵坐标轴线颜色
                            }
                        },
                        axisLabel: {
                            color: '#0DF5F8',
                            fontSize: 8,
                        },
                        axisTick: {
                            inside: true,
                            alignWithLabel: true,
                            interval: 0,
                            color: '#2B427F'
                        },
                        splitLine: {
                            lineStyle: {
                                color: '#2B427F'
                            }
                        },
                        max: 1,
                    },
                    {
                        type: 'value',
                        // name: this.data.data[1].name, // 第二个数据系列的纵坐标轴名称
                        // nameTextStyle: {
                        //     color: this.data.data[1].color // 第二个数据系列的纵坐标轴名称颜色
                        // },
                        axisLine: {
                            lineStyle: {
                                color: this.data.data[1].color // 第二个数据系列的纵坐标轴线颜色
                            }
                        },
                        axisLabel: {
                            color: '#0DF5F8',
                            fontSize: 8,
                        },
                        axisTick: {
                            inside: true,
                            alignWithLabel: true,
                            interval: 0,
                            color: '#2B427F'
                        },
                        splitLine: {
                            lineStyle: {
                                color: '#2B427F'
                            }
                        },
                        max: 21, // 指定最大值为 21
                    }
                ],
                series: [
                    {
                        type: 'bar',
                        name: this.data.data[0].name,
                        barWidth: 4,
                        barGap: 0,
                        itemStyle: {
                            barBorderRadius: 2,
                            color: this.data.data[0].color
                        },
                        yAxisIndex: 0, // 使用第一个纵坐标轴
                        data: this.data.data[0].value
                    },
                    {
                        type: 'bar',
                        name: this.data.data[1].name,
                        barWidth: 4,
                        barGap: 0,
                        itemStyle: {
                            barBorderRadius: 2,
                            color: this.data.data[1].color
                        },
                        yAxisIndex: 1, // 使用第二个纵坐标轴
                        data: this.data.data[1].value
                    },
                ]

            };
            let myChart = this.$echarts(this.$el);

            myChart.clear();
            myChart.resize()
            myChart.setOption(option);
        }
    },
    mounted() {
        this.setChart();
    },
}
</script>
