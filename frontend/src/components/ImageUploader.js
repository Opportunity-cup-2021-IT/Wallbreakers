import React from 'react';
import axios from 'axios';
// import Chart from "react-google-charts";
import './ImageUploader.css'
// import background from './zanuda.png';

async function _handleSubmitChange(name, len) {

    let response = await fetch('http://a726-84-237-54-180.ngrok.io/change', {
        method: 'POST',
        body: JSON.stringify({'id': name, 'len': len})
    })
    let text = await response.json();
    console.log(text)
    return text
}

export default class ImageUpload extends React.Component {
    constructor(props) {
        super(props);
        this.state = {file: '',imagePreviewUrl: '', name: '', len: '', counter: 0, tasks_cost: '', tasks_len: '', tasks: []};
    }

     _handleSubmit(e) {
        const formData = new FormData();

        formData.append(
            "myFile",
            this.state.file,
            this.state.file.name
        );

        axios.post(
            "http://a726-84-237-54-180.ngrok.io/upload", formData,
        )

        // let text = await response.json();
        // console.log(text)

        this.setState({counter: 2})
    }

    _handleImageChange(e) {
        e.preventDefault();

        let reader = new FileReader();
        let file = e.target.files[0];

        reader.onloadend = () => {
            this.setState({
                file: file,
                imagePreviewUrl: reader.result
            });
        }

        reader.readAsDataURL(file)
    }

    render() {
        return (
            <div className="Container">
                {this.state.counter === 0 && <button className="Button" onClick={() => this.setState({counter: 1})}>Загрузить таблицу</button>}
                {this.state.counter === 1 && <div className="previewComponent">
                    <form className="FileChoose" onSubmit={(e)=>this._handleSubmit(e)} encType={'multipart/form-data'}>
                        <input className="fileInput, FileInputLocation"
                               type="file"
                               onChange={(e)=>this._handleImageChange(e)} />
                        <button className="SendButton"
                                type="submit"
                                onClick={(e)=>this._handleSubmit(e)}>Загрузить</button>
                    </form>
                </div>}
                {this.state.counter === 2 && <button className="LoadTable" onClick={() => this.setState({counter: 3})}>Изменить параметры</button>}

                {this.state.counter === 3 && <div className="move">
                    <form className="Load">
                        <label>Введите id изменяемой работы {}
                            <input className="OpacityChange"
                                type="text"
                                // value={this.state.name}
                                onChange={(e) => this.setState({name: e.target.value})}
                            />
                        </label>
                        <label>Введите новую продолжительность работы (в днях) {}
                            <input className="OpacityChange"
                                type="text"
                                // value={this.state.len}
                                onChange={(e) => this.setState({len: e.target.value})}
                            />
                        </label>
                    </form>
                    <button className="LoadButton" onClick={async () => {
                        let text = await _handleSubmitChange(this.state.name, this.state.len)
                        this.setState({tasks_cost: text['cost']})
                        this.setState({tasks_len: text['tasks_len']})
                        this.setState({tasks: text['tasks']})
                        this.setState({counter: 4})
                    }
                    }>Отправить</button>
                </div>}
                {this.state.counter === 4 && <div className="ResultText">
                    <div>Траты составят: {this.state.tasks_cost}</div>
                    <div>Необходимо сдвинуть задач: {this.state.tasks_len}</div>
                </div>}
                {/*{this.state.counter === 4 && <button className="GetResult">Получить результаты</button>}*/}

                {/*{this.state.counter === 5 && <Chart className="gant"*/}
                {/*    width={'100vw'}*/}
                {/*    height={'700vh'}*/}
                {/*    //*/}
                {/*    chartType="Gantt"*/}
                {/*    loader={<div>Loading Chart</div>}*/}
                {/*    data={[*/}
                {/*        [*/}
                {/*            {type: 'string', label: 'Task ID'},*/}
                {/*            {type: 'string', label: 'Task Name'},*/}
                {/*            {type: 'date', label: 'Start Date'},*/}
                {/*            {type: 'date', label: 'End Date'},*/}
                {/*            {type: 'number', label: 'Duration'},*/}
                {/*            {type: 'number', label: 'Percent Complete'},*/}
                {/*            {type: 'string', label: 'Dependencies'},*/}
                {/*        ],*/}
                {/*        [*/}
                {/*            'Task1',*/}
                {/*            'Task1',*/}
                {/*            new Date(2022, 1, 1),*/}
                {/*            new Date(2022, 1, 5),*/}
                {/*            4,*/}
                {/*            // 3 * 24 * 60 * 60 * 1000,*/}
                {/*            100,*/}
                {/*            null,*/}
                {/*        ],*/}
                {/*        [*/}
                {/*            'Task2',*/}
                {/*            'Task2',*/}
                {/*            new Date(2022, 1, 1),*/}
                {/*            new Date(2022, 1, 2),*/}
                {/*            1,*/}
                {/*            100,*/}
                {/*            null,*/}
                {/*        ],*/}
                {/*        [*/}
                {/*            'Task3',*/}
                {/*            'Task3',*/}
                {/*            new Date(2022, 1, 6),*/}
                {/*            new Date(2022, 1, 8),*/}
                {/*            1 * 24 * 60 * 60 * 1000,*/}
                {/*            100,*/}
                {/*            'Task1',*/}
                {/*        ],*/}
                {/*        [*/}
                {/*            'Task4',*/}
                {/*            'Task4',*/}
                {/*            new Date(2022, 1, 10),*/}
                {/*            new Date(2022, 1, 13),*/}
                {/*            1 * 24 * 60 * 60 * 1000,*/}
                {/*            100,*/}
                {/*            'Task3',*/}
                {/*        ],*/}
                {/*        [*/}
                {/*            'Task5',*/}
                {/*            'Task5',*/}
                {/*            new Date(2022, 1, 13),*/}
                {/*            new Date(2022, 1, 16),*/}
                {/*            1 * 24 * 60 * 60 * 1000,*/}
                {/*            100,*/}
                {/*            'Task4',*/}
                {/*        ],*/}
                {/*        [*/}
                {/*            'Task6',*/}
                {/*            'Task6',*/}
                {/*            new Date(2022, 1, 14),*/}
                {/*            new Date(2022, 1, 20),*/}
                {/*            1 * 24 * 60 * 60 * 1000,*/}
                {/*            100,*/}
                {/*            'Task4',*/}
                {/*        ],*/}
                {/*        [*/}
                {/*            'Task7',*/}
                {/*            'Task7',*/}
                {/*            new Date(2022, 1, 15),*/}
                {/*            new Date(2022, 1, 22),*/}
                {/*            1 * 24 * 60 * 60 * 1000,*/}
                {/*            100,*/}
                {/*            'Task4',*/}
                {/*        ],*/}
                {/*        [*/}
                {/*            'Task8',*/}
                {/*            'Task8',*/}
                {/*            new Date(2022, 1, 13),*/}
                {/*            new Date(2022, 1, 20),*/}
                {/*            1 * 24 * 60 * 60 * 1000,*/}
                {/*            100,*/}
                {/*            'Task3',*/}
                {/*        ],*/}
                {/*        [*/}
                {/*            'Task9',*/}
                {/*            'Task9',*/}
                {/*            new Date(2022, 1, 16),*/}
                {/*            new Date(2022, 1, 17),*/}
                {/*            1 * 24 * 60 * 60 * 1000,*/}
                {/*            100,*/}
                {/*            'Task3,Task10',*/}
                {/*        ],*/}
                {/*        [*/}
                {/*            'Task10',*/}
                {/*            'Task10',*/}
                {/*            new Date(2022, 1, 15),*/}
                {/*            new Date(2022, 1, 16),*/}
                {/*            1 * 24 * 60 * 60 * 1000,*/}
                {/*            100,*/}
                {/*            'Task11',*/}
                {/*        ],*/}
                {/*        [*/}
                {/*            'Task11',*/}
                {/*            'Task11',*/}
                {/*            new Date(2022, 1, 3),*/}
                {/*            new Date(2022, 1, 5),*/}
                {/*            1 * 24 * 60 * 60 * 1000,*/}
                {/*            100,*/}
                {/*            'Task2',*/}
                {/*        ],*/}
                {/*        [*/}
                {/*            'Task12',*/}
                {/*            'Task12',*/}
                {/*            new Date(2022, 1, 31),*/}
                {/*            new Date(2022, 1, 35),*/}
                {/*            1 * 24 * 60 * 60 * 1000,*/}
                {/*            100,*/}
                {/*            'Task13',*/}
                {/*        ],*/}
                {/*        [*/}
                {/*            'Task13',*/}
                {/*            'Task13',*/}
                {/*            new Date(2022, 1, 25),*/}
                {/*            new Date(2022, 1, 30),*/}
                {/*            1 * 24 * 60 * 60 * 1000,*/}
                {/*            100,*/}
                {/*            'Task9,Task7',*/}
                {/*        ]*/}
                {/*    ]}*/}
                {/*    rootProps={{'data-testid': '1'}}*/}
                {/*/>}*/}
            </div>
        )
    }
}