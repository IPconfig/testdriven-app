import React from 'react';
import { shallow } from 'enzyme';
import renderer from 'react-test-renderer';

import Overview from '../Overview';

const tube_states = [
    [2,3],
    [1,1,1,1],
    [2,2,2,2],
    [3,3,3,3],
    [4,4,4,4],
    [5,5,5,5],
    [0,4]
];

test('Overview renders properly', () => {
    const wrapper = shallow(<Overview tube_states={tube_states}/>);
 //   expect(wrapper.find('h1').get(0).props.children).toBe('Reactor Overview');
    // reactor
    const reactor = wrapper.find('.reactor');
    expect(reactor.length).toBe(1);
    // reactor rows
    const rows = wrapper.find('.reactor-row');
    expect(rows.length).toBe(7);
    // tubes
    expect(rows.get(0).props.children.length).toBe(2);
    expect(rows.get(1).props.children.length).toBe(4);
    expect(rows.get(2).props.children.length).toBe(4);
    expect(rows.get(3).props.children.length).toBe(4);
    expect(rows.get(4).props.children.length).toBe(4);
    expect(rows.get(5).props.children.length).toBe(4);
    expect(rows.get(6).props.children.length).toBe(2);
});

test('Overview renders a snapshot properly', () => {
    const tree = renderer.create(<Overview tube_states={tube_states}/>).toJSON();
    expect(tree).toMatchSnapshot();
})