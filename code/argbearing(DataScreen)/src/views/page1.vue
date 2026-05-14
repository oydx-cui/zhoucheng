<template>
    <Row class="page1">
        <Col style="width:24%;">
        <div class="left-1">
            <div v-if="loading">Loading...</div>
            <div v-else class="left1-1">
                <span class='title'><span class="title-6">轴承状态</span></span>
                <span class="angle1"></span>
                <span class="angle2"></span>
                <span class="angle3"></span>
                <span class="angle4"></span>
                <seamlessVS ref="seam1" :data="jsonData"></seamlessVS>
            </div>
        </div>
        <div class="left-2">
            <div v-if="loading">Loading...</div>
            <div v-else class="left1-1">
                <span class='title'><span class="title-6">电机负载</span></span>
                <span class="angle1"></span>
                <span class="angle2"></span>
                <span class="angle3"></span>
                <span class="angle4"></span>
                <single-area-chart ref="chart1" :selectRangeDate="selectRangeDate"></single-area-chart>
            </div>
        </div>
        </Col>
        <Col style="width:52%;padding:0 1%;">
        <div class="center-top">
            <div v-if="loading">Loading...</div>
            <div v-else class="center-t1">
                <span class='title'><span class="title-6">轴承故障点</span></span>
                <span class="angle1"></span>
                <span class="angle2"></span>
                <span class="angle3"></span>
                <span class="angle4"></span>
                <!-- <radar-part ref="chart2"></radar-part> -->
                <sliderHP ref="chart2" :data="jsonData"></sliderHP>
            </div>
        </div>
        <div class="center-bottom">
            <div v-if="loading">Loading...</div>
            <div v-else class="center-b1">
                <span class='title'><span class="title-6">故障分布</span></span>
                <span class="angle1"></span>
                <span class="angle2"></span>
                <span class="angle3"></span>
                <span class="angle4"></span>
                <Col style="width:22%">
                <bar-chart ref="chart15" :data="barcData1"></bar-chart>
                </Col>
                <Col style="width:22%">
                <bar-chart ref="chart16" :data="barcData2"></bar-chart>
                </Col>
                <Col style="width:29%">
                <pie ref="chart17" id="pie_1" :data="pieData1"></pie>
                </Col>
                <Col style="width:30%">
                <pie ref="chart18" id="pie_2" :data="pieData2"></pie>
                </Col>
            </div>
        </div>
        </Col>
        <Col style="width:24%">
        <div class="right-all">
            <row style="height: 25%;">
                <div v-if="loading">Loading...</div>
                <div v-else class="right1-1">
                    <span class='title'><span class="title-6">轴承故障排名</span></span>
                    <span class="angle1"></span>
                    <span class="angle2"></span>
                    <span class="angle3"></span>
                    <span class="angle4"></span>
                    <!-- <single-area-chart ref="chart1" :selectRangeDate="selectRangeDate"></single-area-chart> -->
                    <Col style="width:33%">
                    <double-bar :data="data1" ref="chart3"></double-bar>
                    </Col>
                    <Col style="width:33%">
                    <double-bar :data="data2" ref="chart4"></double-bar>
                    </Col>
                    <Col style="width:33%">
                    <double-bar :data="data3" ref="chart5"></double-bar>
                    </Col>
                </div>
            </row>
            <row style="height: 25%;">
                <div v-if="loading">Loading...</div>
                <div v-else class="right1-1">
                    <!-- <span class='title'><span class="title-6">轴承故障排名</span></span> -->
                    <span class="angle1"></span>
                    <span class="angle2"></span>
                    <span class="angle3"></span>
                    <span class="angle4"></span>
                    <!-- <single-area-chart ref="chart1" :selectRangeDate="selectRangeDate"></single-area-chart> -->
                    <Col style="width:33%">
                    <double-bar :data="data4" ref="chart6"></double-bar>
                    </Col>
                    <Col style="width:33%">
                    <double-bar :data="data5" ref="chart7"></double-bar>
                    </Col>
                    <Col style="width:33%">
                    <double-bar :data="data6" ref="chart8"></double-bar>
                    </Col>
                    <!-- <Col style="width:33%">
                            <device-safe-risk ref='deviceSafeRisk'></device-safe-risk>
                        </Col> -->
                </div>
            </row>
            <row style="height: 25%;">
                <div v-if="loading">Loading...</div>
                <div v-else class="right1-1">
                    <!-- <span class='title'><span class="title-6">轴承故障排名</span></span> -->
                    <span class="angle1"></span>
                    <span class="angle2"></span>
                    <span class="angle3"></span>
                    <span class="angle4"></span>
                    <!-- <single-area-chart ref="chart1" :selectRangeDate="selectRangeDate"></single-area-chart> -->
                    <Col style="width:33%">
                    <double-bar :data="data7" ref="chart9"></double-bar>
                    </Col>
                    <Col style="width:33%">
                    <double-bar :data="data8" ref="chart10"></double-bar>
                    </Col>
                    <Col style="width:33%">
                    <double-bar :data="data9" ref="chart11"></double-bar>
                    </Col>
                    <!-- <Col style="width:33%">
                            <device-safe-risk ref='deviceSafeRisk'></device-safe-risk>
                        </Col> -->
                </div>
            </row>
            <row style="height: 25%;">
                <div v-if="loading">Loading...</div>
                <div v-else class="right1-1">
                    <!-- <span class='title'><span class="title-6">轴承故障排名</span></span> -->
                    <span class="angle1"></span>
                    <span class="angle2"></span>
                    <span class="angle3"></span>
                    <span class="angle4"></span>
                    <!-- <single-area-chart ref="chart1" :selectRangeDate="selectRangeDate"></single-area-chart> -->
                    <Col style="width:33%">
                    <double-bar :data="data10" ref="chart12"></double-bar>
                    </Col>
                    <Col style="width:33%">
                    <double-bar :data="data11" ref="chart13"></double-bar>
                    </Col>
                    <Col style="width:33%">
                    <double-bar :data="data12" ref="chart14"></double-bar>
                    </Col>
                    <!-- <Col style="width:33%">
                            <device-safe-risk ref='deviceSafeRisk'></device-safe-risk>
                        </Col> -->
                </div>
            </row>
        </div>
        <!-- <div class="right-2">
                <div class="right1-1">
                    <span class='title'><span class="title-6">轴承故障分布</span></span>
                    <span class="angle1"></span>
                    <span class="angle2"></span>
                    <span class="angle3"></span>
                    <span class="angle4"></span>
                    <red-pocket ref="redPocket"></red-pocket>
                </div>
            </div> -->
        </Col>
    </Row>
</template>

<script>
const singleAreaChart = () => import('./components/singleAreaChart');
const doubleBar = () => import('./components/doubleBar');
const seamlessVS = () => import('./components/seamlessVState');
const sliderHP = () => import('./components/sliderHPic');
const barChart = () => import('./components/barChart');
const pie = () => import('./components/pie');
import axios from 'axios';

export default {
    name: 'page1',
    props: {
        selectRangeDate: Array
    },
    components: {
        // radarPart,
        // redPocket,
        singleAreaChart,
        doubleBar,
        // deviceSafeRisk,
        seamlessVS,
        sliderHP,
        barChart,
        pie
    },
    data() {
        return {
            jsonData: {}, // 定义用于存储JSON数据的变量
            data1: {
                title: 'Bearing-1',
                xname: [],
                data: [
                    {
                        name: '得分',
                        color: '#00CCFF',
                        value: [],
                    },
                    {
                        name: '直径',
                        color: '#142AFE',
                        value: []
                    }
                ]
            },
            data2: {
                title: 'Bearing-2',
                xname: [],
                data: [
                    {
                        name: '得分',
                        color: '#00CCFF',
                        value: [],
                    },
                    {
                        name: '直径',
                        color: '#142AFE',
                        value: []
                    }
                ]
            },
            data3: {
                title: 'Bearing-3',
                xname: [],
                data: [
                    {
                        name: '得分',
                        color: '#00CCFF',
                        value: [],
                    },
                    {
                        name: '直径',
                        color: '#142AFE',
                        value: []
                    }
                ]
            },
            data4: {
                title: 'Bearing-4',
                xname: [],
                data: [
                    {
                        name: '得分',
                        color: '#6514FF',
                        value: [],
                    },
                    {
                        name: '直径',
                        color: '#B370FD',
                        value: []
                    }
                ]
            },
            data5: {
                title: 'Bearing-5',
                xname: [],
                data: [
                    {
                        name: '得分',
                        color: '#6514FF',
                        value: [],
                    },
                    {
                        name: '直径',
                        color: '#B370FD',
                        value: []
                    }
                ]
            },
            data6: {
                title: 'Bearing-6',
                xname: [],
                data: [
                    {
                        name: '得分',
                        color: '#6514FF',
                        value: [],
                    },
                    {
                        name: '直径',
                        color: '#B370FD',
                        value: []
                    }
                ]
            },
            data7: {
                title: 'Bearing-7',
                xname: [],
                data: [
                    {
                        name: '得分',
                        color: '#05467D',
                        value: [],
                    },
                    {
                        name: '直径',
                        color: '#52B8FF',
                        value: []
                    }
                ]
            },
            data8: {
                title: 'Bearing-8',
                xname: [],
                data: [
                    {
                        name: '得分',
                        color: '#05467D',
                        value: [],
                    },
                    {
                        name: '直径',
                        color: '#52B8FF',
                        value: []
                    }
                ]
            },
            data9: {
                title: 'Bearing-9',
                xname: [],
                data: [
                    {
                        name: '得分',
                        color: '#05467D',
                        value: [],
                    },
                    {
                        name: '直径',
                        color: '#52B8FF',
                        value: []
                    }
                ]
            },
            data10: {
                title: 'Bearing-10',
                xname: [],
                data: [
                    {
                        name: '得分',
                        color: '#FD9800',
                        value: [],
                    },
                    {
                        name: '直径',
                        color: '#FDC673',
                        value: []
                    }
                ]
            },
            data11: {
                title: 'Bearing-11',
                xname: [],
                data: [
                    {
                        name: '得分',
                        color: '#FD9800',
                        value: [],
                    },
                    {
                        name: '直径',
                        color: '#FDC673',
                        value: []
                    }
                ]
            },
            data12: {
                title: 'Bearing-12',
                xname: [],
                data: [
                    {
                        name: '得分',
                        color: '#FD9800',
                        value: [],
                    },
                    {
                        name: '直径',
                        color: '#FDC673',
                        value: []
                    }
                ]
            },
            pieData1: {// 饼图数据1
                title: "故障位置",
                color: '#2C7BFE',

                data: [
                    {
                        value: 60,
                        name: '滚珠',
                        itemStyle: {
                            color: '#1456FE'
                        }

                    },
                    {
                        value: 20,
                        name: '内圈',
                        itemStyle: {
                            color: '#00CCFF'
                        }
                    },
                    {
                        value: 80,
                        name: '外圈3',
                        itemStyle: {
                            color: '#142AFE'
                        }
                    },
                    {
                        value: 40,
                        name: '外圈6',
                        itemStyle: {
                            color: '#1493FE'
                        }
                    }
                ],
            },
            pieData2: {// 饼图数据1
                title: "故障直径",
                color: '#2C7BFE',

                data: [
                    {
                        value: 60,
                        name: '正常',
                        itemStyle: {
                            color: '#142AFE'
                        }

                    },
                    {
                        value: 20,
                        name: '7mils',
                        itemStyle: {
                            color: '#1493FE'
                        }
                    },
                    {
                        value: 80,
                        name: '14mils',
                        itemStyle: {
                            color: '#252448'
                        }
                    },
                    {
                        value: 40,
                        name: '21mils',
                        itemStyle: {
                            color: '#00CCFF'
                        }
                    }
                ],
            },
            barcData1: {
                xname: ["滚珠", "内圈", "外圈3", "外圈6"],
                yname: '故障位置次数',
                ydata: [3, 9, 1, 9]
            },
            barcData2: {
                // xname: ['正常', '7mils', '14mils', '21mils'],
                xname: ['7mils', '14mils', '21mils'],
                yname: '故障直径次数',
                ydata: [2, 6, 6]
            },
            loading: true,
        }
    },
    methods: {
        fetchData() {
            // 创建一个包含参数的FormData对象
            const formData = new FormData();
            formData.append('machineNumber', 1);
            // 定义存储故障位置出现次数的对象
            let faultLocCount = {
                '0': 0,
                '1': 0,
                '2': 0,
                '3': 0
            };
            // 初始化记录故障直径出现次数的对象
            let faultDiameterCount = {
                '0': 0,
                '1': 0,
                '2': 0,
                '3': 0
            };
            // 发送POST请求
            axios.post('http://localhost/select_machinebearinginfo.php', formData)
                .then(response => {
                    // 请求成功处理服务器返回的JSON数据
                    console.log('response: ', response.data);
                    this.jsonData = response.data;
                    console.log('jsonData: ', this.jsonData);
                    // 遍历所有的键
                    Object.keys(this.jsonData).forEach(key => {
                        const data = this.jsonData[key];
                        const lastIndex = data.length - 1;

                        // 获取最后一个数据项
                        const lastData = data[lastIndex];

                        // 将键值对应的数据存储到processedData中
                        this["data" + key].xname[0] = (["滚珠", "内圈", "外圈3", "外圈6"][parseInt(lastData.faultLoc1)]);
                        this["data" + key].xname[1] = (["滚珠", "内圈", "外圈3", "外圈6"][parseInt(lastData.faultLoc2)]);
                        this["data" + key].xname[2] = (["滚珠", "内圈", "外圈3", "外圈6"][parseInt(lastData.faultLoc3)]);
                        // this["data" + key].data[0].value[0] = (parseFloat(lastData.faultScore1));
                        // this["data" + key].data[0].value[1] = (parseFloat(lastData.faultScore2));
                        // this["data" + key].data[0].value[2] = (parseFloat(lastData.faultScore3));
                        // this["data" + key].data[1].value[0] = (parseInt(lastData.faultDia1));
                        // this["data" + key].data[1].value[1] = (parseInt(lastData.faultDia2));
                        // this["data" + key].data[1].value[2] = (parseInt(lastData.faultDia3));
                        this["data" + key].data[0].value[0] = parseFloat(lastData.faultScore1).toFixed(3).toString();
                        this["data" + key].data[0].value[1] = parseFloat(lastData.faultScore2).toFixed(3).toString();
                        this["data" + key].data[0].value[2] = parseFloat(lastData.faultScore3).toFixed(3).toString();
                        this["data" + key].data[1].value[0] = ([0, 7, 14, 21][lastData.faultDia1]);
                        this["data" + key].data[1].value[1] = ([0, 7, 14, 21][lastData.faultDia2]);
                        this["data" + key].data[1].value[2] = ([0, 7, 14, 21][lastData.faultDia3]);

                        // 统计故障位置出现次数
                        if (lastData.faultDia1 !== '0') faultLocCount[lastData.faultLoc1]++;
                        if (lastData.faultDia2 !== '0') faultLocCount[lastData.faultLoc2]++;
                        if (lastData.faultDia3 !== '0') faultLocCount[lastData.faultLoc3]++;

                        // 统计故障直径出现次数
                        faultDiameterCount[lastData.faultDia1]++;
                        faultDiameterCount[lastData.faultDia2]++;
                        faultDiameterCount[lastData.faultDia3]++;

                    });
                    console.log('data1: ', this.data1);

                    // 将统计结果保存在 piedata1 中
                    this.pieData1.data[0].value = faultLocCount['0'];
                    this.pieData1.data[1].value = faultLocCount['1'];
                    this.pieData1.data[2].value = faultLocCount['2'];
                    this.pieData1.data[3].value = faultLocCount['3'];
                    console.log('pieData1: ', this.pieData1);

                    // 将统计结果保存在 piedata2 中
                    this.pieData2.data[0].value = faultDiameterCount['0'];
                    this.pieData2.data[1].value = faultDiameterCount['1'];
                    this.pieData2.data[2].value = faultDiameterCount['2'];
                    this.pieData2.data[3].value = faultDiameterCount['3'];
                    console.log('pieData2: ', this.pieData2);

                    this.barcData1.ydata[0] = faultLocCount['0'];
                    this.barcData1.ydata[1] = faultLocCount['1'];
                    this.barcData1.ydata[2] = faultLocCount['2'];
                    this.barcData1.ydata[3] = faultLocCount['3'];
                    console.log('barcData1: ', this.barcData1);

                    // this.barcData2.ydata[0] = faultDiameterCount['0'];
                    // this.barcData2.ydata[1] = faultDiameterCount['1'];
                    // this.barcData2.ydata[2] = faultDiameterCount['2'];
                    // this.barcData2.ydata[3] = faultDiameterCount['3'];

                    this.barcData2.ydata[0] = faultDiameterCount['1'];
                    this.barcData2.ydata[1] = faultDiameterCount['2'];
                    this.barcData2.ydata[2] = faultDiameterCount['3'];

                    console.log('barcData2: ', this.barcData2);

                    for (let i = 1; i <= 18; i++) {
                        this.$refs['chart' + i].setChart();
                    }

                    this.loading = false;
                })
                .catch(error => {
                    // 请求失败处理错误
                    console.error('Error fetching data:', error);

                    this.loading = false;
                });
        }
    },
    watch: {},
    mounted() {
        this.fetchData();
        this.resizeFn = this.$debounce(() => {
            // 通过捕获系统的onresize事件触发我们需要执行的事件
            for (let i = 1; i <= 18; i++) {
                this.$refs['chart' + i].setChart();
            }
        }, 500)
        window.addEventListener('resize', this.resizeFn)

    },
    beforeDestroy() {
        window.removeEventListener('resize', this.resizeFn)
    }

}

</script>

<style lang="less">
.page1 {
    height: 100%;
    width: 100%;
    padding: 14px 20px 20px;
    background: #03044A;
    overflow: hidden;

    .ivu-col {
        height: 100%;
        float: left;
    }

    .left1-1,
    .right1-1,
    .center-t1,
    .center-b1 {
        height: 100%;
        border: 1px solid #0D2451;
        position: relative;
        background: #151456;
    }

    .center-top {
        height: 60%;

        .center-t1 {
            height: 92%;
            display: flex;
            justify-content: center
        }
    }

    .center-bottom {
        height: 40%;

        .center-b1 {
            display: flex;
            justify-content: center
        }
    }

    .left-1 {
        height: 60%;

        .left1-1 {
            height: 92%;
            display: flex;
            justify-content: center
        }
    }

    .left-2 {
        height: 40%;
    }

    .right-1 {
        height: 50%;

        .right1-1 {
            height: 92%;
        }
    }

    .right-2 {
        height: 50%;
    }

    .right-all {
        height: 100%;
    }
}
</style>
