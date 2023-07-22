function add_variant() {
  'use_strict'
  let fields_count = Number(count.innerHTML)
  let new_input =  document.createElement('input')
  let new_input2 =  document.createElement('input')
  new_input.name = `add_answer_${fields_count}`
  new_input.name = `add_param_${fields_count}`
  new_input.required = true
  new_input.style.marginTop = '3px'
  new_input.classList.add('styled-text-input');
  new_input2.required = true
  new_input2.style.marginTop = '3px'
  new_input2.classList.add('styled-text-input');
  new_input.id = `add_answer_${fields_count}`
  new_input.id = `add_param_${fields_count}`
  param_container.appendChild(new_input)
  variants_container.appendChild(new_input2)

  new_input.focus()
  new_input2.focus()

  count.innerHTML = String(fields_count+1)
}
