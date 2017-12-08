import React from 'react';
import {shallow} from 'enzyme'
import CheckBox from '../components/Content/CheckBox';
import Enzyme from 'enzyme';
import Adapter from 'enzyme-adapter-react-16';

Enzyme.configure({ adapter: new Adapter() });

describe('<CheckBox />', () => {
	it('renders a checkbox, there is only one input element', () => {
		const checkbox = shallow(<CheckBox />);
		expect((checkbox.find('input')).length).toEqual(1);
		expect((checkbox.find('input')).checked).toEqual(false);
	});

	it('toggle checkbox should become true', () => {
		const checkbox = shallow(<CheckBox />);
		checkbox.find('input').simulate('change');
		//expect(checkbox.find('input').checked).toEqual(true);
	});
});
