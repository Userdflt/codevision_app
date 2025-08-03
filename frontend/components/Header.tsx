import { User } from '@supabase/supabase-js'
import { Fragment } from 'react'
import { Menu, Transition } from '@headlessui/react'
import { UserCircleIcon, ChevronDownIcon } from '@heroicons/react/24/outline'

interface HeaderProps {
  user?: User
  onSignOut: () => void
}

export default function Header({ user, onSignOut }: HeaderProps) {
  return (
    <header className="bg-white shadow-sm border-b border-gray-200">
      <div className="container mx-auto px-4">
        <div className="flex justify-between items-center h-16">
          {/* Logo */}
          <div className="flex items-center">
            <h1 className="text-xl font-bold text-gray-900">
              Code Vision
            </h1>
            <span className="ml-2 text-sm text-gray-500">
              AI Building Code Assistant
            </span>
          </div>

          {/* User Menu */}
          {user && (
            <div className="flex items-center">
              <Menu as="div" className="relative">
                <Menu.Button className="flex items-center text-sm text-gray-700 hover:text-gray-900">
                  <UserCircleIcon className="h-8 w-8 mr-2" />
                  <span className="hidden md:block">
                    {user.email}
                  </span>
                  <ChevronDownIcon className="h-4 w-4 ml-1" />
                </Menu.Button>

                <Transition
                  as={Fragment}
                  enter="transition ease-out duration-100"
                  enterFrom="transform opacity-0 scale-95"
                  enterTo="transform opacity-100 scale-100"
                  leave="transition ease-in duration-75"
                  leaveFrom="transform opacity-100 scale-100"
                  leaveTo="transform opacity-0 scale-95"
                >
                  <Menu.Items className="absolute right-0 mt-2 w-48 origin-top-right bg-white rounded-md shadow-lg ring-1 ring-black ring-opacity-5 focus:outline-none">
                    <div className="py-1">
                      <Menu.Item>
                        {({ active }) => (
                          <button
                            onClick={onSignOut}
                            className={`${
                              active ? 'bg-gray-100' : ''
                            } block w-full text-left px-4 py-2 text-sm text-gray-700`}
                          >
                            Sign Out
                          </button>
                        )}
                      </Menu.Item>
                    </div>
                  </Menu.Items>
                </Transition>
              </Menu>
            </div>
          )}
        </div>
      </div>
    </header>
  )
}