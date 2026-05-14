<template>
    <vue-seamless-scroll :data="listData" class="seamless-warp" :class-option="defaultOption">
        <ul class="item">
            <li v-for="item in listData" :key="item.id">
                <span class="date" v-text="item.date"></span>
                <span class="id" v-text="item.id"></span>
                <span
                    :class="{ 'state': true, 'normal': item.state === '正常', 'abnormal': item.state === '异常', 'defective': item.state === '缺陷' }"
                    v-text="item.state"></span>
            </li>
        </ul>
    </vue-seamless-scroll>
</template>

<style lang="less" scoped>
.seamless-warp {
    height: 86%;
    line-height: 20px;
    overflow: hidden;
    position: relative;
    margin-top: 8%
}

.date,
.id,
.state {
    display: inline-block;
    color: #6EDDF1;
    // background: #14418E;
    font-size: 15px;
    padding: 5px 8px;
}

.id {
    width: 92px;
    text-align: center;
}

.normal {
    color: green;
    /* 设置正常状态下的字体颜色为绿色 */
}

.abnormal {
    color: red;
    /* 设置异常状态下的字体颜色为红色 */
}

.defective {
    color: yellow;
    /* 设置缺陷状态下的字体颜色为黄色 */
}
</style>

<script>
export default {
    props: {
        data: Object
    },
    data() {
        return {
            listData: [{
                'id': 'Bearing-1',
                'date': '2024-03-27 13:00:00',
                'state': '正常'
            }, {
                'id': 'Bearing-2',
                'date': '2024-03-27 13:00:00',
                'state': '正常'
            }, {
                'id': 'Bearing-3',
                'date': '2024-03-27 13:00:00',
                'state': '缺陷'
            }, {
                'id': 'Bearing-4',
                'date': '2024-03-27 13:00:00',
                'state': '异常'
            }, {
                'id': 'Bearing-5',
                'date': '2024-03-27 13:00:00',
                'state': '正常'
            }, {
                'id': 'Bearing-6',
                'date': '2024-03-27 13:00:00',
                'state': '异常'
            }, {
                'id': 'Bearing-7',
                'date': '2024-03-27 13:00:00',
                'state': '正常'
            }, {
                'id': 'Bearing-8',
                'date': '2024-03-27 13:00:00',
                'state': '正常'
            }, {
                'id': 'Bearing-9',
                'date': '2024-03-27 13:00:00',
                'state': '异常'
            }, {
                'id': 'Bearing-10',
                'date': '2024-03-27 13:00:00',
                'state': '正常'
            }, {
                'id': 'Bearing-11',
                'date': '2024-03-27 13:00:00',
                'state': '正常'
            }, {
                'id': 'Bearing-12',
                'date': '2024-03-27 13:00:00',
                'state': '正常'
            }]
        }
    },
    computed: {
        defaultOption() {
            return {
                step: 0.5, // 数值越大速度滚动越快
                limitMoveNum: 8, // 开始无缝滚动的数据量 this.dataList.length
                hoverStop: true, // 是否开启鼠标悬停stop
                direction: 1, // 0向下 1向上 2向左 3向右
                openWatch: true, // 开启数据实时监控刷新dom
                singleHeight: 0, // 单步运动停止的高度(默认值0是无缝不停止的滚动) direction => 0/1
                singleWidth: 0, // 单步运动停止的宽度(默认值0是无缝不停止的滚动) direction => 2/3
                waitTime: 1000 // 单步运动停止的时间(默认值1000ms)
            }
        }
    },
    mounted() {
        // 清空listData
        this.listData = [];

        // 遍历data中的键值对
        for (const key in this.data) {
            if (Object.hasOwnProperty.call(this.data, key)) {
                const data = this.data[key];
                const lastData = data[data.length - 1];

                // 将数字后缀转换成字符串
                const id = 'Bearing-' + key;

                // 根据最后一个 JSON 数据设置 state
                let state = '正常';
                if (lastData.faultDia1 !== '0' || lastData.faultDia2 !== '0' || lastData.faultDia3 !== '0') {
                    state = '缺陷';
                }
                if (lastData.faultDia1 === '3' || lastData.faultDia2 === '3' || lastData.faultDia3 === '3') {
                    state = '异常';
                }

                // 添加新的数据项到listData中
                this.listData.push({
                    id: id,
                    date: lastData.detectTime,
                    state: state
                });
            }
        }
    }
    ,
    methods: {
    }
}
</script>
