password_bag = set()

### Neighbour Swaps
def swap_neighbours(pwds, num_swaps):
    result = rec_swap_n(pwds, num_swaps)
    password_bag.update(result)
    print('Dictionary of', len(password_bag), 'generated with neighbour swaps using max of', num_swaps, 'swaps.')
def rec_swap_n(passwords, number_of_swaps):
    if number_of_swaps <= 0:
        return passwords
    for _ in range(number_of_swaps):
        step_pwds = set()
        for pwd in passwords:
            for i in range(len(pwd) - 1):
                #print('swaps', swap(pwd, i, i+1))
                step_pwds.add(swap(pwd, i, i+1))
        passwords.update(step_pwds)

    return passwords
def swap(s, l, r):
    return s[0:l] + s[r] + s[l+1:r] + s[l] + s[r+1:]


### Shift Misuses
def shift_misuses(pwds, num_misuses):
    if num_misuses <= 0:
        return pwds
    for _ in range(num_misuses):
        step_pwds = set()
        for pwd in pwds:
            for i in range(len(pwd)):
                if i == len(pwd)-1:
                    shift_apply = pwd[0:i] + apply_single_shift_misuse(pwd[i])
                else:
                    shift_apply = pwd[0:i] + apply_single_shift_misuse(pwd[i]) + pwd[i+1:]
                #print('shift', shift_apply)
                step_pwds.add(shift_apply)
        pwds.update(step_pwds)

    print('Dictionary of', len(pwds), 'generated with shift misues using max of', num_misuses, 'shift misuses.')
    return pwds



numeric_swaps = {'1': '!', '2': '@', '3': '#', '4': '$', '5': '%', '6': '^', '7': '&', '8': '*', '9': '(', '0': ')'}
def apply_single_shift_misuse(s):
    return numeric_swaps.get(s) if s.isnumeric() else s.lower()

### Keyboard duplication (malfunctions)
def keyboard_duplicates(pwds, num_duplication_events, max_repetition_force):
    if max_repetition_force <= 1:
        return pwds
    if num_duplication_events <= 0:
        return pwds
    for _ in range(num_duplication_events):
        step_pwds = set()
        for pwd in pwds:
            for i in range(len(pwd)):
                if i == len(pwd)-1:
                    key_duplication = pwd[0:i] + pwd[i] + pwd[i]
                    step_pwds.add(key_duplication)
                    # print('duplication', key_duplication)
                else:
                    for repetition_force in range(2, max_repetition_force + 1):
                        key_duplication = pwd[0:i] + repetition_force * pwd[i] + pwd[i+1:]
                        step_pwds.add(key_duplication)
                        # print('duplication', key_duplication)
        pwds.update(step_pwds)

    print('Dictionary of', len(pwds), 'generated with key duplication using max of', num_duplication_events,
          'duplication events and', max_repetition_force, 'max repetition force.')
    return pwds


if __name__ == '__main__':
    word1 = 'ABCDE'
    word2 = 'FGHIJKL'
    number_suffix = '123'
    initpass = word1 + word2 + number_suffix

    password_bag.add(initpass)
    swap_neighbours(password_bag, 1)
    shift_misuses(password_bag, 1)
    keyboard_duplicates(password_bag, 1, 4)

    output_file = open("passphrases.txt", "w")
    output_file.write(str(password_bag))
    output_file.close()
