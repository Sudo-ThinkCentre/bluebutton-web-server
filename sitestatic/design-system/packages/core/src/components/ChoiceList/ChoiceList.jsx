import Choice from './Choice';
import FormLabel from '../FormLabel/FormLabel';
import PropTypes from 'prop-types';
import React from 'react';
import Select from './Select';
import classNames from 'classnames';
import uniqueId from 'lodash.uniqueid';

/**
 * A `ChoiceList` component can be used to render a select menu, radio
 * button group, or checkbox group.
 *
 * By default the component determines the type of field for you, taking
 * into account accessibility and usability best practices. So, you can pass in
 * an array of `choices` and let it determine what type of field would be best for
 * the user, or alternatively you can manually pass in the `type` prop.
 */
export class ChoiceList extends React.PureComponent {
  /**
   * Creates the field component(s) based on the type of field we've determined
   * it should be.
   */
  field() {
    const type = this.type();
    const ChoiceComponent = type === 'select' ? 'option' : Choice;
    const selectProps = {};

    const choices = this.props.choices.map(choice => {
      const { checked, defaultChecked, label, ...props } = choice;

      if (type === 'select') {
        if (checked) selectProps.value = props.value;
        if (defaultChecked) selectProps.defaultValue = props.value;
      } else {
        props.checked = checked;
        props.defaultChecked = defaultChecked;
        // Individual choices can be disabled as well as the entire list.
        // We only need to check for both options on checkbox/radio fields,
        // since the <Select> component handles the case where the entire list
        // is disabled.
        props.disabled = props.disabled || this.props.disabled;
        props.inversed = this.props.inversed;
        props.name = this.props.name;
        props.onBlur = this.props.onBlur;
        props.onChange = this.props.onChange;
        props.type = type;
      }

      return (
        <ChoiceComponent key={choice.value} {...props}>
          {label}
        </ChoiceComponent>
      );
    });

    if (type === 'select') {
      return this.select(selectProps, choices);
    }

    return choices;
  }

  /**
   * If this is a <select> element, then we need to generate the ID here
   * so it can be shared between the FormLabel and Select component
   */
  id() {
    // ID will be generated by the Choice component
    if (this.type() !== 'select') return;

    if (!this._id) {
      // Cache the ID so we're not regenerating it on each method call
      this._id = uniqueId(`select_${this.props.name}_`);
    }

    return this._id;
  }

  /**
   * @param {object} selectProps
   * @param {array} options - <option> components
   */
  select(selectProps, options) {
    return (
      <Select
        disabled={this.props.disabled}
        id={this.id()}
        inversed={this.props.inversed}
        name={this.props.name}
        onBlur={this.props.onBlur}
        onChange={this.props.onChange}
        {...selectProps}
      >
        {options}
      </Select>
    );
  }

  /**
   * Determines the type of field(s) we should render based on a few factors
   */
  type() {
    if (this.props.type) {
      return this.props.type;
    }

    if (this.props.multiple || this.props.choices.length === 1) {
      // Prefer a checkbox when multiple choices can be selected, since users
      // have trouble selecting multiple choices from a select menu. And if only
      // one choice is available, then a radio button would prevent a user from
      // deselecting the field.
      return 'checkbox';
    } else if (this.props.choices.length > 7) {
      // Prefer a select menu when the list has "many" choices.
      // TODO(sawyer): More research needed to determine what's considered "many"
      return 'select';
    }

    return 'radio';
  }

  render() {
    const type = this.type();
    const classes = classNames(
      { 'ds-c-fieldset': type !== 'select' },
      this.props.className
    );
    const RootComponent = type === 'select' ? 'div' : 'fieldset';
    const FormLabelComponent = type === 'select' ? 'label' : 'legend';

    return (
      <RootComponent className={classes || null}>
        <FormLabel
          className={this.props.labelClassName}
          component={FormLabelComponent}
          errorMessage={this.props.errorMessage}
          fieldId={this.id()}
          hint={this.props.hint}
          requirementLabel={this.props.requirementLabel}
          inversed={this.props.inversed}
        >
          {this.props.label}
        </FormLabel>
        {this.field()}
      </RootComponent>
    );
  }
}

ChoiceList.propTypes = {
  /**
   * The list of choices to be rendered. The number of choices you pass in may
   * affect the type of field(s) rendered. See `type` for more info.
   */
  choices: PropTypes.arrayOf(
    PropTypes.shape({
      checked: Choice.propTypes.checked,
      defaultChecked: Choice.propTypes.defaultChecked,
      disabled: Choice.propTypes.disabled,
      label: Choice.propTypes.children,
      value: Choice.propTypes.value,
      requirementLabel: PropTypes.oneOfType([PropTypes.string, PropTypes.node])
    })
  ).isRequired,
  /**
   * Additional classes to be added to the root element.
   */
  className: PropTypes.string,
  /**
   * Disables the entire field.
   */
  disabled: PropTypes.bool,
  errorMessage: PropTypes.string,
  /**
   * Additional hint text to display
   */
  hint: PropTypes.node,
  /**
   * Text showing the requirement ("Required", "Optional", etc.). See [Required and Optional Fields]({{root}}/guidelines/forms/#required-and-optional-fields).
   */
  requirementLabel: PropTypes.oneOfType([PropTypes.string, PropTypes.node]),
  /**
   * Applies the "inverse" UI theme
   */
  inversed: PropTypes.bool,
  /**
   * Label for the field
   */
  label: PropTypes.node.isRequired,
  /**
   * Additional classes to be added to the `FormLabel`.
   */
  labelClassName: PropTypes.string,
  /**
   * Allows the user to select multiple choices. Setting this to `true` results
   * in a list of checkbox fields to be rendered.
   */
  multiple: PropTypes.bool,
  /**
   * The field's `name` attribute
   */
  name: PropTypes.string.isRequired,
  onBlur: PropTypes.func,
  onChange: PropTypes.func,
  /**
   * You can manually set the `type` if you prefer things to be less magical.
   * Otherwise, the type will be inferred by the other `props`, based
   * on what's best for accessibility and usability. If `multiple` is `true`, then
   * `checkbox` fields will be rendered. If less than 10 choices are passed in,
   * then `radio` buttons will be rendered.
   */
  type: PropTypes.oneOf(['checkbox', 'radio', 'select'])
};

export default ChoiceList;
