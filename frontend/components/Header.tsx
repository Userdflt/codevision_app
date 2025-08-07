import { Fragment } from 'react'
import { Menu, Transition } from '@headlessui/react'
import { UserCircleIcon, ChevronDownIcon } from '@heroicons/react/24/outline'
import { User } from '@supabase/supabase-js'
import { LogoIcon } from './logo'

interface HeaderProps {
  user?: User | null
  onSignOut?: () => void
}

export default function Header({ user, onSignOut }: HeaderProps) {
  return (
    <header className="bg-background border-b border-border shadow-sm">
      <div className="container mx-auto px-4">
        <div className="flex justify-between items-center h-16">
          {/* Logo */}
          <div className="flex items-center">
            <LogoIcon />
            <div className="ml-3">
              <h1 className="text-xl font-bold text-foreground">
                Code Vision
              </h1>
              <span className="text-sm text-muted-foreground">
                AI Building Code Assistant
              </span>
            </div>
          </div>

          {/* User Menu */}
          {user && (
            <div className="flex items-center">
              <Menu as="div" className="relative">
                <Menu.Button className="flex items-center text-sm text-foreground hover:text-muted-foreground">
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
                  <Menu.Items className="absolute right-0 mt-2 w-48 origin-top-right bg-popover rounded-md shadow-lg ring-1 ring-border focus:outline-none">
                    <div className="py-1">
                      <Menu.Item>
                        {({ active }) => (
                          <button
                            onClick={onSignOut}
                            className={`${
                              active ? 'bg-accent' : ''
                            } block w-full text-left px-4 py-2 text-sm text-popover-foreground`}
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